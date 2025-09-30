import time
import ast
import importlib
import tempfile
import os
import inspect
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class CodingTool:
    name: str
    description: str
    function_code: str
    parameters: Dict[str, Any]
    created_at: float
    is_active: bool = False


class SelfCodingTool:
    def __init__(self, agent):

        self.generated_tools: Dict[str, CodingTool] = {}
        self.temp_dir = tempfile.mkdtemp(prefix="coding_tools_")

        self.tool_creator = agent

    def create_tool(self, requirement: str, context: Dict[str, Any] = None) -> CodingTool:
        """Create Tool based on requirements"""
        if context is None:
            context = {}

        tool_name = f"custom_tool_{int(time.time())}"

        tool_code = self._generate_tool_code(requirement, tool_name)

        tool = CodingTool(
            name=tool_name,
            description=requirement,
            function_code=tool_code,
            parameters={},
            created_at=time.time()
        )

        if self._validate_tool(tool):

            return self._get_tool(tool)

        else:
            print(" Tool validation failed")

    def _generate_tool_code(self, requirement: str, tool_name: str) -> str:
        """Generate Tool code"""
        code_prompt = f"""
        Create a Python function based on the following requirements:
        
        Requirement: {requirement}
        
        Requirements:
        1. The function name MUST be exactly: {tool_name}
        2. Include explicit Python type hints for ALL parameters and return type
        3. Use only safe operations, no filesystem/network unless required
        4. Provide complete error handling and clear exceptions
        5. Include a detailed, concise docstring describing parameters and return types
        6. Keep code concise and efficient
        
        Only return the function code, no other content.
        """

        code_response = self.tool_creator.chat(code_prompt)

        # Clean code response
        code = code_response.strip()
        if code.startswith('```python'):
            code = code[9:]
        if code.startswith('```'):
            code = code[3:]
        if code.endswith('```'):
            code = code[:-3]

        return code.strip()

    def _validate_tool(self, tool: CodingTool) -> bool:
        """Validate Tool"""
        try:
            # Syntax check
            ast.parse(tool.function_code)
            return True
        except SyntaxError:
            return False

    def _get_tool(self, tool: CodingTool):
        """Register Tool to Agent"""
        try:
            # Create temporary file
            temp_file = os.path.join(self.temp_dir, f"{tool.name}.py")
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(tool.function_code)

            # Dynamic import
            spec = importlib.util.spec_from_file_location(tool.name, temp_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Get function
            func = getattr(module, tool.name)

            # Build JSON schema parameters from function annotations
            annotations = getattr(func, "__annotations__", {}) or {}
            return_type = annotations.pop("return", None)
            signature = inspect.signature(func)

            def python_type_to_json_schema(py_type: Any) -> str:
                try:
                    # Handle typing origins like list[str]
                    origin = getattr(py_type, "__origin__", None)
                    if origin is list or origin is List:
                        return "array"
                    if origin is dict or origin is Dict:
                        return "object"
                except Exception:
                    pass
                if py_type in (str, bytes):
                    return "string"
                if py_type in (int,):
                    return "integer"
                if py_type in (float,):
                    return "number"
                if py_type in (bool,):
                    return "boolean"
                if py_type in (list, tuple, set):
                    return "array"
                if py_type in (dict,):
                    return "object"
                # default fallback
                return "string"

            properties: Dict[str, Dict[str, Any]] = {}
            required_params: List[str] = []
            for param_name, param in signature.parameters.items():
                if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                    # Skip *args/**kwargs from required list and set as array/object accordingly
                    json_type = "array" if param.kind == inspect.Parameter.VAR_POSITIONAL else "object"
                    properties[param_name] = {
                        "type": json_type,
                        "description": f"Auto-inferred parameter {param_name}"
                    }
                    continue
                anno = annotations.get(param_name, str)
                json_type = python_type_to_json_schema(anno)
                properties[param_name] = {
                    "type": json_type,
                    "description": f"Auto-inferred parameter {param_name}"
                }
                if param.default is inspect._empty:
                    required_params.append(param_name)

            # Create Tool definition
            tool_definition = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": required_params
                    },
                    "function": func
                }
            }

            return tool_definition["function"]

        except Exception as e:
            print(f"Tool registration failed: {str(e)}")
            return False

from typing import Any, Dict, List, Optional, Union, get_type_hints, get_origin, get_args
from enum import Enum
import inspect

def get_function_parameters(func) -> Dict[str, Any]:

    annotations: Dict[str, Any] = getattr(func, "__annotations__", {}) or {}
    signature = inspect.signature(func)

    properties: Dict[str, Any] = {}
    required: list[str] = []

    for name, param in signature.parameters.items():
        if name == 'self':
            continue
        # Determine type (fallback to Any -> string) from annotations
        param_type = annotations.get(name, Any)
        properties[name] = _generate_param_schema(param_type,f"Parameter {name}")
        # Required if no default specified
        if param.default is inspect.Parameter.empty:
            required.append(name)

    return {
        "type": "object",
        "properties": properties,
        "required": required
    }




def _generate_param_schema(param_type: Any, description: str) -> Dict[str, Any]:
    """Generate JSON schema for a parameter type."""
    schema = {"description": description}
    
    # Handle different type annotations
    if param_type == str or param_type == Optional[str] or param_type == Union[str, None]:
        schema["type"] = "string"
    elif param_type == int or param_type == Optional[int] or param_type == Union[int, None]:
        schema["type"] = "integer"
    elif param_type == float or param_type == Optional[float] or param_type == Union[float, None]:
        schema["type"] = "number"
    elif param_type == bool or param_type == Optional[bool] or param_type == Union[bool, None]:
        schema["type"] = "boolean"
    elif param_type == list or param_type == List or param_type == Optional[list]:
        schema["type"] = "array"
        schema["items"] = {"type": "string"}
    elif param_type == dict or param_type == Dict or param_type == Optional[dict]:
        schema["type"] = "object"
    elif param_type == Any:
        schema["type"] = "string"  # Default to string for Any type
    else:
        # Handle complex types
        origin = get_origin(param_type)
        args = get_args(param_type)
        
        if origin is Union:
            # Handle Union types (including Optional)
            non_none_types = [t for t in args if t is not type(None)]
            if non_none_types:
                return _generate_param_schema(non_none_types[0], description)
            else:
                schema["type"] = "string"
        elif origin is list or origin is List:
            schema["type"] = "array"
            if args:
                schema["items"] = _generate_param_schema(args[0], "item")
            else:
                schema["items"] = {"type": "string"}
        elif origin is dict or origin is Dict:
            schema["type"] = "object"
        elif hasattr(param_type, '__origin__') and param_type.__origin__ is Union:
            # Handle Union types
            non_none_types = [t for t in param_type.__args__ if t is not type(None)]
            if non_none_types:
                return _generate_param_schema(non_none_types[0], description)
            else:
                schema["type"] = "string"
        elif isinstance(param_type, type) and issubclass(param_type, Enum):
            schema["type"] = "string"
            schema["enum"] = [e.value for e in param_type]
        else:
            # Fallback to string for unknown types
            schema["type"] = "string"
    
    return schema




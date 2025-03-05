def solidity_to_openai_type(solidity_type):
    base_type = solidity_type.rstrip("[]")
    is_array = solidity_type.endswith("[]")

    if base_type == "bool":
        return "array" if is_array else "boolean"

    if base_type.startswith(("int", "uint")):
        return "array" if is_array else "integer"

    if base_type == "address":
        return "array" if is_array else "string"

    if base_type.startswith("bytes") or base_type == "string":
        return "array" if is_array else "string"

    if "[" in base_type and "]" in base_type:
        return "array"

    if base_type.startswith("mapping") or base_type in ["struct", "enum"]:
        return "object"

    return "string"


# Helper function to safely serialize objects
def safe_serialize(obj):
    if obj is None:
        return None
    elif hasattr(obj, "__dict__"):
        # For objects with __dict__, try to extract basic info
        try:
            if hasattr(obj, "name"):
                return {"name": obj.name, "type": type(obj).__name__}
            else:
                return {"type": type(obj).__name__}
        except:
            return {"type": type(obj).__name__}
    else:
        return str(obj)

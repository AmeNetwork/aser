def get_model_from(model_name):
    if model_name.lower().startswith("gpt"):
        return "openai"
    else:
        return "unknown"
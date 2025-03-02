def get_model_from(model_name):
    if model_name.lower().startswith("gpt"):
        return "openai"
    elif model_name.lower().startswith("deepseek"):
        return "deepseek"
    else:
        return "unknown"
def get_model_from(model_name):
    model_name = model_name.lower() 
    if 'gpt' in model_name:
        return 'openai'
    elif 'claude' in model_name:
        return 'anthropic'
    elif 'deepseek' in model_name:
        return 'deepseek'
    else:
        return 'unknown' 
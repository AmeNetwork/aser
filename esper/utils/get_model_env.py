import os
def get_model_env(model_name):
    model_name = model_name.lower() 
    model_env={
        "base_url":"",
        "api_key":""
    }
    if 'gpt' in model_name:
        model_env["base_url"]=os.getenv("OPENAI_API_BASE")
        model_env["api_key"]=os.getenv("OPENAI_KEY")
        
    elif 'claude' in model_name:
        model_env["base_url"]=os.getenv("ANTHROPIC_API_BASE")
        model_env["api_key"]=os.getenv("ANTHROPIC_KEY")

    elif 'deepseek' in model_name:
        model_env["base_url"]=os.getenv("DEEPSEEK_API_BASE")
        model_env["api_key"]=os.getenv("DEEPSEEK_KEY")
    
    elif 'grok' in model_name:
        model_env["base_url"]=os.getenv("XAI_API_BASE")
        model_env["api_key"]=os.getenv("XAI_KEY")
    
    elif 'gemini' in model_name:
        model_env["base_url"]=os.getenv("GEMINI_API_BASE")
        model_env["api_key"]=os.getenv("GEMINI_KEY")

    else:
        raise ValueError("model not supported")

    return model_env
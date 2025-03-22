import os
def knowledge_to_prompt(knowledge, text):
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    knowledge_result = knowledge.query(text)

    formatted_results = []
    
    if (knowledge_result.get('documents') and knowledge_result.get('metadatas') and 
        len(knowledge_result['documents'][0]) == len(knowledge_result['metadatas'][0])):
        
        for i, (document, metadata) in enumerate(zip(knowledge_result['documents'][0], knowledge_result['metadatas'][0])):
            metadata_str = ", ".join(f"{k}:{v}" for k, v in metadata.items())
            formatted_result = f"{i+1}. {document} {metadata_str}."
            formatted_results.append(formatted_result)
        
    return "\n".join(formatted_results)



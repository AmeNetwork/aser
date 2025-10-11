import json
def load_character(path: str):
    with open(path, 'r', encoding='utf-8') as file:
        character_data = json.load(file)
    json_string = json.dumps(character_data, ensure_ascii=False)
    return json_string
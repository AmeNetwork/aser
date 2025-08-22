from pathlib import Path
def get_file_data(path):
    suffix=Path(path).suffix
    if suffix in [".txt",".md",".log"]:
        with open(path, 'r') as f:
            data = f.read()
    else:
        data = ''
    return data
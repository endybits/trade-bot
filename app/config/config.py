import os
import json

path_file = 'app/config/config.json'

def get_openai_apikey():
    if not os.path.exists(path_file):
        raise FileNotFoundError(f'The config file {path_file} is missing.')    
    return json.loads(open(path_file, 'r', encoding="UTF-8").read())

OPENAI_APIKEY = get_openai_apikey()
print(OPENAI_APIKEY)
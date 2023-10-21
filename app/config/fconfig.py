import os
import json

path_file = 'app/config/config.json'

def get_config_values():
    if not os.path.exists(path_file):
        raise FileNotFoundError(f'The config file {path_file} is missing.')    
    return json.loads(open(path_file, 'r', encoding="UTF-8").read())

CONFIG_VALUES = get_config_values()


def get_openai_apikey():
    return CONFIG_VALUES.get('openai_api_key')

def get_db_credentials():
    return CONFIG_VALUES.get('db')
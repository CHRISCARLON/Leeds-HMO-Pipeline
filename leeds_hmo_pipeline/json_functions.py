import json 
from loguru import logger

def current_local_date(json_path): 
    with open(json_path, 'r') as file:
        data = json.load(file)
        current_value = data.get('current', '')
        return current_value
    
def update_json(json_path, new_string):
    with open(json_path, 'w') as file:
        json.dump({'current': new_string}, file)
    logger.info("JSON file updated with new date:", new_string)
import os
import json
# from pathlib import Path

def write_to_json(json_obj, file='gpt_response.json'):
    # p = Path(directory)
    # p.mkdir(parents=True, exist_ok=True)
    if not os.path.exists(file): # create file not exist and write empty list
        with open(file , 'w+') as f:
            json.dump([], f)
    with open(file) as f:
        json_list = json.load(f)
        json_list.append(json_obj) # need to be not a dict
    with open(file, 'w') as f:
        json.dump(json_list, f, separators=(',', ': '), indent=4)
    # print(f"Write to {file} successfully!")


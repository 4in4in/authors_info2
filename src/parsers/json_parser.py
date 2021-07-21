
import json
import os

class JsonParser:
    jsons_path = './jsons'

    @classmethod
    def read_json(cls, file_name):
        with open(f'{cls.jsons_path}/{file_name}', 'r') as f:
            result = json.load(f)
            return result

    @classmethod
    def save_to_json(cls, data_to_save, file_name):
        with open(f'{cls.jsons_path}/{file_name}', 'w') as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)

    @classmethod
    def check_json_existing(cls, file_name):
        return os.path.isfile(f'{cls.jsons_path}/{file_name}')
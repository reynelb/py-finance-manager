import json
import os

FILE_PATH = "data.json"

class Storage:
    @staticmethod
    def load():
        if not os.path.exists(FILE_PATH):
            return {"transactions": []}
        with open(FILE_PATH, "r") as file:
            return json.load(file)

    @staticmethod
    def save(data):
        with open(FILE_PATH, "w") as file:
            json.dump(data, file, indent=4)

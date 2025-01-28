import json

RESOURCES_PATH = "./tests/resources"


def read_json_file(file_path) -> dict:

    with open(f"{RESOURCES_PATH}/{file_path}", "r") as file:
        return json.load(file)

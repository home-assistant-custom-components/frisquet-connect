import json

RESOURCES_PATH = "./tests/resources"


def read_json_file_as_json(file_path) -> dict:
    return json.loads(read_json_file_as_text(file_path))


def read_json_file_as_text(file_path) -> str:
    with open(f"{RESOURCES_PATH}/{file_path}.json", "r") as file:
        return file.read()

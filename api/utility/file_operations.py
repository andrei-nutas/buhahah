import json

import importlib_resources

RESOURCES_DIRECTORY = importlib_resources.files("payloads")
DOCUMENTS_DIRECTORY = RESOURCES_DIRECTORY / "documents"

def load_json(filename):
    with open(RESOURCES_DIRECTORY / filename, "r") as file:
        project_data = json.load(file)
        print(project_data)
        return project_data

def open_pdf(filename):
    with open(DOCUMENTS_DIRECTORY / filename, "rb") as file:
        return file.read()

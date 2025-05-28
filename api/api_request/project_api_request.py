import logging
import time
from datetime import datetime

from playwright.sync_api import APIRequestContext

from api.api_request.endpoints import Endpoint
from api.utility.file_operations import open_pdf
from api.utility.mime_type import MimeType

class ProjectApi:

    def __init__(self, request_context: APIRequestContext):
        self.request_context = request_context

    def create_project(self):
        logging.info("Create project")
        response = self.request_context.post(url = Endpoint.get("project"))
        assert response.ok, f"API request failed: {response.json()}"
        return response.json()

    def update_project(self, project_id: str, payload):
        payload["project_title"] = payload["project_title"] + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = self.request_context.patch(url = Endpoint.get("project_id",
                                                                 paths = {"project_id": project_id}),
                                              data = payload)
        assert response.ok, f"API request failed: {response.json()}"
        return response.json()

    def get_project_by_id_response(self, project_id: str):
        response = self.get_project_by_id(project_id)
        assert response.ok, f"API request failed: {response.json()}"
        return response.json()

    def get_project_by_id(self, project_id: str):
        return self.request_context.get(url = Endpoint.get("project_id",
                                                           paths = {"project_id": project_id}))

    def get_projects_response(self):
        response = self.get_projects()
        assert response.ok, f"API request failed: {response.json()}"
        return response.json()

    def get_projects(self):
        return self.request_context.get(url = Endpoint.get("project"))

    def upload_document(self, project_id: str, filename: str, mime_type: MimeType):
        response = self.request_context.post(
            url = Endpoint.get("project_document",
                               paths = {"project_id": project_id}),
            params = {"file_type": "file"},
            multipart = {"file":
                             {"name": filename,
                              "mimeType": mime_type.value,
                              "buffer": open_pdf(filename)
                              }})
        assert response.ok, f"API request failed: {response.json()}"
        return response.json()

    def extract_information(self, project_id: str):
        logging.info("Extract information/ Process RFP")
        response = self.request_context.patch(url = Endpoint.get("project_process_rfp",
                                                                 paths = {"project_id": project_id}))
        assert response.ok, f"API request failed: {response.json()}"
        return response.json()

    def create_storyline_structure(self, project_id: str):
        logging.info("Create storyline and structure")
        response = self.request_context.patch(
            url = Endpoint.get("project_storyline_structure", paths = {"project_id": project_id}))
        assert response.ok, f"API request failed: {response.json()}"
        return response.json()

    def generate_content(self, project_id: str):
        logging.info("Generate content/pitch")
        response = self.request_context.patch(
            url = Endpoint.get("project_generate_content", paths = {"project_id": project_id}))
        assert response.ok, f"API request failed: {response.json()}"
        return response.json()

    def wait_processing_finish(self, project_id: str, attribute: str, timeout: int = 360, poll_interval: float = 3.0):
        start_time = time.time()

        while True:
            project_response = self.get_project_by_id_response(project_id)
            is_processing = project_response.get("processing", True)
            custom_value = project_response.get(attribute)

            if not is_processing and custom_value is not None:
                logging.info("Process finished after %d seconds", time.time() - start_time)
                break

            if time.time() - start_time > timeout:
                raise TimeoutError(f"Timeout error! Field '{attribute}' not populated after {timeout} seconds")

            time.sleep(poll_interval)

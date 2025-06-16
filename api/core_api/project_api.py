import json
import logging
import time
from datetime import datetime

from api.common.client_adapters import BaseAdapter 
from api.common.response_adapter import AbstractAdapterResponse
from api.endpoints import Endpoint
from api.utility.file_operations import open_pdf 
from api.utility.mime_type import MimeType

class ProjectApi:
    #TODO: split the api functions into various dedicated files in the next step
    def __init__(self, adapter: BaseAdapter):
        self.adapter = adapter

    def create_project_raw(self) -> AbstractAdapterResponse:
        logging.info("Create project")
        # Not specifically requested for plotting by user count, so no generic name passed here.
        # It will appear in Locust stats with its full URL.
        return self.adapter.post(url=Endpoint.get("project"))

    def create_project(self) -> dict:
        response = self.create_project_raw()
        assert response.ok, f"API request failed: {response.status_code} - {response.text}"
        return response.json()

    def update_project_raw(self, project_id: str, payload: dict) -> AbstractAdapterResponse:
        payload["project_name"] = payload["project_name"] + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        url = Endpoint.get("project_id", paths={"project_id": project_id})
        # Not specifically requested for plotting, using full URL for Locust name.
        return self.adapter.patch(url=url, json=payload) 

    def update_project(self, project_id: str, payload: dict) -> dict:
        response = self.update_project_raw(project_id, payload)
        assert response.ok, f"API request failed: {response.status_code} - {response.text}"
        return response.json()

    def get_project_by_id_raw(self, project_id: str) -> AbstractAdapterResponse:
        url = Endpoint.get("project_id", paths={"project_id": project_id})
        # Polling requests for wait_processing_finish use this.
        # You could give this a generic name like "project/get_by_id" if you want to track its performance too.
        return self.adapter.get(url=url) 

    def get_project_by_id_response(self, project_id: str) -> dict:
        response = self.get_project_by_id_raw(project_id)
        assert response.ok, f"API request failed: {response.status_code} - {response.text}"
        return response.json()

    def get_projects_raw(self) -> AbstractAdapterResponse:
        return self.adapter.get(url=Endpoint.get("project")) # Name will be the URL "project"

    def get_projects_response(self) -> dict:
        response = self.get_projects_raw()
        assert response.ok, f"API request failed: {response.status_code} - {response.text}"
        return response.json()

    def upload_document_raw(self, project_id: str, filename: str, mime_type: MimeType) -> AbstractAdapterResponse:
        # 1. Prepare the JSON metadata for the 'data' field
        json_data_payload = {
            "type": "file",
            "tags": ["primary"],  # Or make this configurable if needed
            "metadata": {"title": filename}, # Use the actual filename here
            "notes": ""  # Or make this configurable
        }

        # 2. Prepare the multipart dictionary for Playwright
        playwright_style_multipart = {
            "data": json.dumps(json_data_payload),  # Send the JSON metadata as a string
            "file": {  # Send the actual file under the 'file' field name
                "name": filename,
                "mimeType": mime_type.value,
                "buffer": open_pdf(filename) # Ensure open_pdf(filename) returns bytes
            }
        }

        url = Endpoint.get("project_document", paths={"project_id": project_id})
        generic_name = "project/document_upload" # Generic name for plotting
        
        return self.adapter.post(
            url=url,
            params={"file_type": "file"}, # This remains as a query parameter
            multipart=playwright_style_multipart,
            name=generic_name
        )

    def upload_document(self, project_id: str, filename: str, mime_type: MimeType) -> dict:
        response = self.upload_document_raw(project_id, filename, mime_type)
        assert response.ok, f"API request failed: {response.status_code} - {response.text}"
        return response.json()

    def extract_overview_raw(self, project_id: str) -> AbstractAdapterResponse:
        logging.info("Exstract overview / start processing")
        url = Endpoint.get("document_start_processing", paths={"project_id": project_id})
        generic_name = "document/start-procesing"
        return self.adapter.post(url=url, name=generic_name)

    def extract_overview(self, project_id: str) -> dict:
        response = self.extract_overview_raw(project_id)
        assert response.ok, f"API request failed: {response.status_code} - {response.text}"
        return response.json() 

    def extract_requierments_raw(self, project_id: str) -> AbstractAdapterResponse: #move to requierments later
        logging.info("Extract project requierments")
        url = Endpoint.get("overview_confirm", paths={"project_id": project_id})
        generic_name = "overview/confirm" # Generic name
        return self.adapter.post(url=url, name=generic_name)

    def extract_requierments(self, project_id: str) -> dict: #move to requierments later
        response = self.extract_requierments_raw(project_id)
        assert response.ok, f"API request failed: {response.status_code} - {response.text}"
        return response.json()

    def generate_epics_raw(self, project_id: str) -> AbstractAdapterResponse:# move to epics later
        logging.info("Generate epics")
        url = Endpoint.get("requirements_confirm", paths={"project_id": project_id})
        generic_name = "requirements/confirm" # Generic name
        return self.adapter.post(url=url, name=generic_name)

    def generate_epics(self, project_id: str) -> dict: #move to epics later
        response = self.generate_epics_raw(project_id)
        assert response.ok, f"API request failed: {response.status_code} - {response.text}"
        return response.json()

    def generate_stories_raw(self, project_id: str) -> AbstractAdapterResponse: #move to stories later
        logging.info("Generate stories")
        url = Endpoint.get("epics_confirm", paths={"project_id": project_id})
        generic_name = "epics/confirm" # Generic name
        return self.adapter.post(url=url, name=generic_name)

    def generate_stories(self, project_id: str) -> dict:
        response = self.generate_stories_raw(project_id)
        assert response.ok, f"API request failed: {response.status_code} - {response.text}"
        return response.json()

    def wait_processing_finish(self, project_id: str, state: str, timeout: int = 360, poll_interval: float = 3.0):
        start_time = time.time()
        logging.info(f"Waiting for processing to finish and state to change to '{state}' on project '{project_id}' (timeout: {timeout}s)...")
        while True:
            project_response_dict = self.get_project_by_id_response(project_id)
            is_processing = project_response_dict.get("processing", True)
            project_state = project_response_dict.get("project_state", state )

            if not is_processing and project_state == state:
                logging.info(f"Process finished for reaching state '{state}' after {time.time() - start_time:.2f} seconds")
                break

            if time.time() - start_time > timeout:
                logging.error(f"Timeout error! State '{state}' not reached or processing did not finish after {timeout} seconds for project '{project_id}'. Current state: {project_response_dict}")
                raise TimeoutError(f"Timeout error! State '{state}' not reached or processing not finished after {timeout} seconds")
            
            logging.debug(f"Still waiting for state '{state}'. Processing: {is_processing}, Current State: {project_state}. Elapsed: {time.time() - start_time:.2f}s")
            time.sleep(poll_interval)
import logging

import pytest
from playwright.sync_api import APIRequestContext
import importlib_resources

from api.api_request.project_api_request import ProjectApi
from api.utility.excel_operations import update_excel_with_extracted_content
from api.utility.file_operations import load_json
from api.utility.mime_type import MimeType

EXCEL_OUTPUT_PATH = importlib_resources.files("extracted_info_output") / "output.xlsx"

EXTRACTED_INFO_ATTR = "extracted_info"
ID_ATTR = "id"

class TestWorkflow:

    @pytest.mark.workflow
    def test_workflow(self, api_request_context: APIRequestContext):
        logging.info("Starting pitch workflow...")
        project_api = ProjectApi(api_request_context)

        rfp_filename = "RFP_CDP_Venture_Capital_SGR.pdf"

        create_project_response = project_api.create_project()
        project_id = create_project_response[ID_ATTR]
        logging.info("Project ID: %s", project_id)

        get_project_by_id_response = project_api.get_project_by_id_response(project_id)
        assert get_project_by_id_response[ID_ATTR] == project_id

        payload = load_json("default.json")
        update_project_response = project_api.update_project(project_id, payload)
        assert update_project_response[ID_ATTR] == project_id

        project_api.upload_document(project_id, rfp_filename, MimeType.PDF)

        project_api.extract_information(project_id)
        project_api.wait_processing_finish(project_id, EXTRACTED_INFO_ATTR)

        project_api.create_storyline_structure(project_id)
        project_api.wait_processing_finish(project_id, "storyline_structure")

        project_api.generate_content(project_id)
        project_api.wait_processing_finish(project_id, "generated_content")

        update_excel_with_extracted_content(EXCEL_OUTPUT_PATH,
                                            project_api.get_project_by_id_response(project_id)[EXTRACTED_INFO_ATTR])

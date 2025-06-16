from api.common.client_adapters import BaseAdapter
from api.common.response_adapter import AbstractAdapterResponse
from api.endpoints import Endpoint

class MyProjectApi:
    def __init__(self, adapter: BaseAdapter):
        self.adapter = adapter

    def get_my_project_raw(self) -> AbstractAdapterResponse:
        return self.adapter.get(url=Endpoint.get("project_mine"))

    def get_my_project_response(self) -> dict:
        response = self.get_my_project_raw()
        assert response.ok, f"API request failed: {response.status_code} - {response.text()}"
        return response.json()

    def delete_incomplete_project_raw(self, project_id: str) -> AbstractAdapterResponse:
        return self.adapter.delete(url=Endpoint.get("my_project_id", paths={"project_id": project_id}))

    def delete_incomplete_project_response(self, project_id: str) -> dict:
        response = self.delete_incomplete_project_raw(project_id)
        assert response.ok, f"API request failed: {response.status_code} - {response.text()}"
        # Assuming API returns a JSON body on successful DELETE based on original code.
        # If it returns 204 No Content, response.json() would fail.
        # Adjust if API returns no body (e.g., return response.text() or None).
        return response.json()
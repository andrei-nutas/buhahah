from playwright.sync_api import APIRequestContext

from api.api_request.endpoints import Endpoint

class MyProjectApi:

    def __init__(self, request_context: APIRequestContext):
        self.request_context = request_context

    def get_my_project_response(self):
        response = self.get_my_project()
        assert response.ok, f"API request failed: {response.json()}"
        return response.json()

    def get_my_project(self):
        return self.request_context.get(url = Endpoint.get("my_project"))

    def get_assigned_projects_response(self):
        response = self.get_assigned_projects()
        assert response.ok, f"API request failed: {response.json()}"
        return response.json()

    def get_assigned_projects(self):
        return self.request_context.get(url = Endpoint.get("my_project_assigned"))

    def delete_incomplete_project_response(self, project_id: str):
        response = self.delete_incomplete_project(project_id)
        assert response.ok, f"API request failed: {response.json()}"
        return response.json()

    def delete_incomplete_project(self, project_id: str):
        return self.request_context.delete(url = Endpoint.get("my_project_id", paths = {"project_id": project_id}))

from playwright.sync_api import APIRequestContext

from api.api_request.endpoints import Endpoint

class UserApi:

    def __init__(self, request_context: APIRequestContext):
        self.request_context = request_context

    def get_current_user_profile_response(self):
        response = self.get_current_user_profile()
        assert response.ok, f"API request failed: {response.json()}"
        return response.json()

    def get_current_user_profile(self):
        return self.request_context.get(url = Endpoint.get("current_user_profile"))

    def logout_user(self):
        response = self.request_context.delete(url = Endpoint.get("logout"))
        assert response.status == 204, f"API request failed: {response.json()}"

    def get_users_response(self):
        response = self.get_users()
        assert response.ok, f"API request failed: {response.json()}"
        return response.json()

    def get_users(self):
        return self.request_context.get(url = Endpoint.get("users"))

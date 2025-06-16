from api.common.client_adapters import BaseAdapter
from api.common.response_adapter import AbstractAdapterResponse
from api.endpoints import Endpoint

class UserApi:
    def __init__(self, adapter: BaseAdapter):
        self.adapter = adapter

    def get_current_user_profile_raw(self) -> AbstractAdapterResponse:
        return self.adapter.get(url=Endpoint.get("current_user_profile"))

    def get_current_user_profile_response(self) -> dict:
        response = self.get_current_user_profile_raw()
        assert response.ok, f"API request failed: {response.status_code} - {response.text()}"
        return response.json()

    def logout_user_raw(self) -> AbstractAdapterResponse:
        return self.adapter.delete(url=Endpoint.get("logout"))

    def logout_user(self):
        response = self.logout_user_raw()
        assert response.status_code == 204, f"API request failed: expected 204, got {response.status_code} - {response.text()}"
        

    def get_users_raw(self) -> AbstractAdapterResponse:
        return self.adapter.get(url=Endpoint.get("users"))

    def get_users_response(self) -> dict:
        response = self.get_users_raw()
        assert response.ok, f"API request failed: {response.status_code} - {response.text()}"
        return response.json()
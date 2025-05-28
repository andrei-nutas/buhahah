import random

import pytest
from playwright.sync_api import APIRequestContext

from api.api_request.my_project_api_request import MyProjectApi
from api.api_request.project_api_request import ProjectApi
from api.api_request.user_api_request import UserApi
from api.config import environment_setup

@pytest.mark.auth
class TestAuthentication:

    # Verify retrieval of the current user's profile with a valid token
    # Preconditions: -
    # Steps:
    #   - Send a GET request to /api/v1/authorize endpoint with the prepared header
    # Expected Results: The response status code is 200 OK and the response body contains the current user
    def test_get_current_user_with_valid_token(self, api_request_context: APIRequestContext):
        user_api = UserApi(api_request_context)
        response = user_api.get_current_user_profile_response()
        assert response["email"] == environment_setup.COGNITO_USERNAME, "Email does not have the expected value"

    # Verify accessing the list of completed projects fails without an authentication token
    # Preconditions:
    #   - Prepare a header without an authentication token
    # Steps:
    #   - Send a GET request to /api/v1/project/ endpoint with the prepared header
    # Expected Results: The response status code is 401 Unauthorized and the response body contains the error "Token is missing"
    def test_access_projects_without_token(self, no_authentication_token: APIRequestContext):
        project_api = ProjectApi(no_authentication_token)
        response = project_api.get_projects()
        self.check_invalid_response(response.status, response.json(), "Token is missing")

    # Verify accessing the user-specific project list fails without an authentication token
    # Preconditions:
    #   - Prepare a header without an authentication token
    # Steps:
    #   - Send a GET request to /api/v1/me/project/ endpoint with the prepared header
    # Expected Results: The response status code is 401 Unauthorized and the response body contains the error "Token is missing"
    def test_access_my_project_without_token(self, no_authentication_token: APIRequestContext):
        my_project_api = MyProjectApi(no_authentication_token)
        response = my_project_api.get_my_project()
        self.check_invalid_response(response.status, response.json(), "Token is missing")

    # Verify accessing a specific project fails with an expired token
    # Preconditions:
    #   - Prepare a header without an authentication token
    # Steps:
    #   - Send a GET request to /api/v1/me/project/ endpoint with the prepared header
    # Expected Results: The response status code is 401 Unauthorized and the response body contains the error "Token is missing"
    def test_access_project_with_expired_token(self, expired_authentication_token: APIRequestContext,
                                               api_request_context: APIRequestContext):
        project_api = ProjectApi(api_request_context)
        project_items = project_api.get_projects_response()["items"]
        random_project_id = random.choice(project_items)["id"]

        project_api = ProjectApi(expired_authentication_token)
        response = project_api.get_project_by_id(random_project_id)
        self.check_invalid_response(response.status, response.json(), "Token has expired")

    # Verify getting the current user profile fails with an invalid/malformed token
    # Preconditions:
    #   - Prepare a header with an invalid authentication token
    # Steps:
    #   - Send a GET request to /api/v1/authorize endpoint with the prepared header
    # Expected Results: The response status code is 401 Unauthorized and the response body contains the error "Invalid token: Not enough segments"
    def test_get_current_user_profile_with_malformed_token(self, malformed_authentication_token: APIRequestContext):
        user_profile = UserApi(malformed_authentication_token)
        response = user_profile.get_current_user_profile()
        self.check_invalid_response(response.status, response.json(), "Invalid token: Not enough segments")

    # Verify accessing the user list fails without authentication
    # Preconditions:
    #   - Prepare a header without an authentication token
    # Steps:
    #   - Send a GET request to /api/v1/users endpoint with the prepared header
    # Expected Results: The response status code is 401 Unauthorized and the response body contains the error "Token is missing"
    def test_get_users_details_without_token(self, no_authentication_token: APIRequestContext):
        user_profile = UserApi(no_authentication_token)
        response = user_profile.get_users()
        self.check_invalid_response(response.status, response.json(), "Token is missing")

    # Verify a token becomes invalid after a successful logout
    # Preconditions: -
    # Steps:
    #   - Send a DELETE request to /api/v1/logout endpoint with a valid token
    #   - Using the same token, send a GET request to /api/v1/authorize endpoint
    # Expected Results: The response status code is 401 Unauthorized and the response body contains the error "Token has been revoked"
    def test_token_is_invalid_after_logout(self, api_request_context: APIRequestContext):
        user_profile = UserApi(api_request_context)
        user_profile.logout_user()

        response = user_profile.get_current_user_profile()
        self.check_invalid_response(response.status, response.json(), "Token has been revoked")

    @staticmethod
    def check_invalid_response(status, body, expected_message):
        assert status == 401
        assert body["detail"] == expected_message, "Detail text is not correct"

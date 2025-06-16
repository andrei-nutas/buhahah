import boto3

from api.config import environment_setup # This imports COGNITO_USERNAME, COGNITO_PASSWORD etc.

# Initialize the Cognito client
client = boto3.client("cognito-idp", region_name=environment_setup.AWS_REGION)

def authenticate_user(username: str, password: str):
    """
    Authenticates a user with AWS Cognito.
    """
    try:
        response = client.initiate_auth(
            ClientId=environment_setup.COGNITO_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password
            }
        )
        return response["AuthenticationResult"]
    except client.exceptions.NotAuthorizedException:
        print("Invalid username or password")
        # Consider raising an exception here or returning None/False
        # to allow calling code to handle the failure.
    except client.exceptions.UserNotFoundException:
        print("User does not exist")
        # Similar handling consideration as above.
    except Exception as e:
        print(f"An unexpected error occurred during authentication: {e}")
        # Similar handling consideration as above.
    return None # Explicitly return None on failure if not raising exception

def get_access_token() -> str | None:
    """
    Retrieves an access token for the configured Cognito user.
    Returns the AccessToken string or None if authentication fails.
    """
    auth_result = authenticate_user(
        environment_setup.COGNITO_USERNAME,
        environment_setup.COGNITO_PASSWORD
    )
    if auth_result and "AccessToken" in auth_result:
        return auth_result["AccessToken"]
    return None

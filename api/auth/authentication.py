import boto3

from api.config import environment_setup

client = boto3.client("cognito-idp", region_name = environment_setup.AWS_REGION)

def authenticate_user(username: str, password: str):
    try:
        response = client.initiate_auth(
            ClientId = environment_setup.COGNITO_CLIENT_ID,
            AuthFlow = "USER_PASSWORD_AUTH",
            AuthParameters = {
                "USERNAME": username,
                "PASSWORD": password
            }
        )
        return response["AuthenticationResult"]
    except client.exceptions.NotAuthorizedException:
        print("Invalid username or password")
    except client.exceptions.UserNotFoundException:
        print("User does not exist")
    except Exception as e:
        print(f"Error: {e}")

def get_access_token():
    return authenticate_user(environment_setup.COGNITO_USERNAME, environment_setup.COGNITO_PASSWORD)["AccessToken"]

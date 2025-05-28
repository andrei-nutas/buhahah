import os

from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
COGNITO_USERNAME = os.getenv("COGNITO_USERNAME")
assert COGNITO_USERNAME, "COGNITO_USERNAME is not set"
COGNITO_PASSWORD = os.getenv("COGNITO_PASSWORD")
assert COGNITO_PASSWORD, "COGNITO_PASSWORD is not set"

BASE_URL = "https://salesstage.nessgen.net/api/v1/"

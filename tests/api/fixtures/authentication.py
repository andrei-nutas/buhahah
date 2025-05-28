from typing import Generator

import pytest
from playwright.sync_api import Playwright, APIRequestContext

from api.auth.authentication import get_access_token
from api.config import environment_setup

@pytest.fixture()
def api_request_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
    }
    request_context = playwright.request.new_context(
        base_url = environment_setup.BASE_URL, extra_http_headers = headers
    )
    yield request_context
    request_context.dispose()

@pytest.fixture(scope = "session")
def no_authentication_token(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(
        base_url = environment_setup.BASE_URL
    )
    yield request_context
    request_context.dispose()

@pytest.fixture(scope = "session")
def expired_authentication_token(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    headers = {
        "Authorization": f"Bearer eyJraWQiOiJlWG4wU1VOS3lENk5YcGNGeDk4dE5LbnhFcWg2N281aFwvT09MY0Vzbjc5OD0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJkMWM5NzBlZS1lMGExLTcwMDEtYzMyMC1iN2RlM2E0YmZkNGEiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0zLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtM19yeWR5Yzg2TTQiLCJjbGllbnRfaWQiOiIzOWk1MTZkN2Q5OHRodWdoZWg1N2NidW8xZiIsIm9yaWdpbl9qdGkiOiIxN2ZlYzE1Ny1mMjZmLTQ3MmUtYjZmYS0wZDFiOGI1MTQ3ZGYiLCJldmVudF9pZCI6IjQ0Y2QzMGI4LTU1NjUtNGE4OS05MDkzLTdmM2IzYTc2N2MwNiIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3NDY1MTkwOTUsImV4cCI6MTc0NjU0NDUwMywiaWF0IjoxNzQ2NTQwOTAzLCJqdGkiOiJhODQ1ZGQwZi04NTU2LTRiMTgtODFlOS0yNTNmODc1MTNlNDkiLCJ1c2VybmFtZSI6ImQxYzk3MGVlLWUwYTEtNzAwMS1jMzIwLWI3ZGUzYTRiZmQ0YSJ9.iElvq3pnLLa-nx4-RAQy1IFdlQhzLXqtlI3ABANkNsosP769XvYfA-7dfmmlO_ULQECcllCZMb-Kzr0k0AiCE79mTzjWXjlztEjtIPTcq_G9Q27i0gaQwAsRXZS5EbtQhHgCEoZJiEvmyKsNHPc6ZidgoxWVMOb1Is1_Ecrf46mn_fT8I7oTFtMR7kKPyFagwYr2UNtrmjMkLko1z5GTkGX4F06tFlB-fSxfbh_WGEs35ShmendoG6KCOeDxc-uHZmFowdDCPQUlR-6r7xR9Qj9mfipmG6kXUb_DHLWsuqii84L5GsycbE5NLVxjEYmpnUeQEytbO2NkcDmfuLsT1g",
    }
    request_context = playwright.request.new_context(
        base_url = environment_setup.BASE_URL, extra_http_headers = headers
    )
    yield request_context
    request_context.dispose()

@pytest.fixture(scope = "session")
def malformed_authentication_token(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    headers = {
        "Authorization": f"Bearer eyJraWQiOiJlWG4wU1VOS3lENk5YcGNGeDk4dE5LbnhFcWg2N281aFwvT09MY0Vzbjc5OD0iLCJhbGc",
    }
    request_context = playwright.request.new_context(
        base_url = environment_setup.BASE_URL, extra_http_headers = headers
    )
    yield request_context
    request_context.dispose()

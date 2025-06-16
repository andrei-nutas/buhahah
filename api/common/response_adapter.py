from abc import ABC, abstractmethod
from playwright.sync_api import APIResponse as PlaywrightAPIResponse

class AbstractAdapterResponse(ABC):
    def __init__(self, underlying_response):
        self._underlying_response = underlying_response

    @property
    @abstractmethod
    def ok(self) -> bool:
        pass

    @abstractmethod
    def json(self) -> dict:
        pass

    @property
    @abstractmethod
    def status_code(self) -> int:
        pass

    @property
    @abstractmethod
    def text(self) -> str:
        pass

    @property
    def underlying_response(self):
        return self._underlying_response

class PlaywrightAdapterResponse(AbstractAdapterResponse):
    def __init__(self, response: PlaywrightAPIResponse):
        super().__init__(response)
        self.response: PlaywrightAPIResponse = response

    @property
    def ok(self) -> bool:
        return self.response.ok

    def json(self) -> dict:
        return self.response.json()

    @property
    def status_code(self) -> int:
        return self.response.status

    @property
    def text(self) -> str:
        return self.response.text()

class LocustAdapterResponse(AbstractAdapterResponse): # Placeholder
    def __init__(self, response): # Replace with actual Locust Response type
        super().__init__(response)
        self.response = response # This would be locust.clients.Response

    @property
    def ok(self) -> bool:
        # Locust's Response.ok might be different or use status_code
        return 200 <= self.response.status_code < 300

    def json(self) -> dict:
        # Locust's response.json() might raise an error if no JSON content
        try:
            return self.response.json()
        except Exception: # Or specific JSONDecodeError from Locust
            # Log error or return empty dict as per requirement
            return {}


    @property
    def status_code(self) -> int:
        return self.response.status_code

    @property
    def text(self) -> str:
        return self.response.text
import logging
from abc import ABC, abstractmethod
from playwright.sync_api import APIRequestContext as PlaywrightAPIRequestContext

from api.common.response_adapter import AbstractAdapterResponse, PlaywrightAdapterResponse

class BaseAdapter(ABC):
    @abstractmethod
    def get(self, url, params=None, headers=None, name: str = None) -> AbstractAdapterResponse:
        pass

    @abstractmethod
    def post(self, url, data=None, json=None, params=None, headers=None, multipart=None, name: str = None) -> AbstractAdapterResponse:
        pass

    @abstractmethod
    def patch(self, url, data=None, json=None, params=None, headers=None, name: str = None) -> AbstractAdapterResponse: # Removed multipart from Base PATCH for simplicity
        pass

    @abstractmethod
    def delete(self, url, params=None, headers=None, name: str = None) -> AbstractAdapterResponse:
        pass

class PlaywrightAdapter(BaseAdapter):
    def __init__(self, request_context: PlaywrightAPIRequestContext):
        self.client = request_context

    def get(self, url, params=None, headers=None, name: str = None) -> PlaywrightAdapterResponse:
        # 'name' parameter is for Locust/custom tracking, not directly used by Playwright client's get
        response = self.client.get(url, params=params, headers=headers)
        return PlaywrightAdapterResponse(response)

    def post(self, url, data=None, json=None, params=None, headers=None, multipart=None, name: str = None) -> PlaywrightAdapterResponse:
        final_data = data
        final_headers = headers.copy() if headers else {}

        if multipart:
            if data or json:
                logging.warning("If 'multipart' is provided, 'data' and 'json' parameters are typically ignored by Playwright's underlying post for multipart. Ensure correct usage.")
            # Playwright handles Content-Type for multipart automatically.
            # Ensure our custom Content-Type for json isn't conflicting.
            if "Content-Type" in final_headers and json is not None:
                 del final_headers["Content-Type"] # Let Playwright set multipart Content-Type
            
            pw_kwargs = {
                "params": params,
                "headers": final_headers if final_headers else None, # Pass None if empty
                "multipart": multipart
            }
            # Remove None values to avoid passing them as kwargs
            pw_kwargs = {k: v for k, v in pw_kwargs.items() if v is not None}
            response = self.client.post(url, **pw_kwargs)

        elif json is not None:
            if data is not None:
                logging.warning("Both 'data' and 'json' provided to PlaywrightAdapter.post; 'json' content will be used as JSON payload.")
            final_data = json # Playwright uses 'data' for the JSON body
            # Ensure Content-Type is application/json, but don't override if already set to something else for a specific reason.
            if not final_headers.get("Content-Type"): 
                final_headers["Content-Type"] = "application/json"
            
            pw_kwargs = {
                "data": final_data, # Playwright will serialize this to JSON if headers indicate so
                "params": params,
                "headers": final_headers if final_headers else None,
            }
            pw_kwargs = {k: v for k, v in pw_kwargs.items() if v is not None}
            response = self.client.post(url, **pw_kwargs)
        else:
            # Default case: use 'data' as is (could be string, bytes, or dict for form data if Content-Type is set)
            pw_kwargs = {
                "data": final_data,
                "params": params,
                "headers": final_headers if final_headers else None,
            }
            pw_kwargs = {k: v for k, v in pw_kwargs.items() if v is not None}
            response = self.client.post(url, **pw_kwargs)
            
        return PlaywrightAdapterResponse(response)

    def patch(self, url, data=None, json=None, params=None, headers=None, name: str = None) -> PlaywrightAdapterResponse:
        # Similar logic to post, typically PATCH uses JSON or form data, less commonly multipart.
        # Playwright's patch method signature allows data, form, multipart.
        final_data = data
        final_headers = headers.copy() if headers else {}

        if json is not None:
            if data is not None:
                logging.warning("Both 'data' and 'json' provided to PlaywrightAdapter.patch; 'json' content will be used as JSON payload.")
            final_data = json 
            if not final_headers.get("Content-Type"):
                final_headers["Content-Type"] = "application/json"
        
        pw_kwargs = {
            "data": final_data,
            "params": params,
            "headers": final_headers if final_headers else None,
        }
        # If you need multipart for PATCH, add similar logic as in post()
        # For example:
        # if multipart is not None:
        #     pw_kwargs["multipart"] = multipart
        #     # Adjust headers if needed, e.g., remove application/json if multipart is set

        pw_kwargs = {k: v for k, v in pw_kwargs.items() if v is not None}
        response = self.client.patch(url, **pw_kwargs)
        return PlaywrightAdapterResponse(response)

    def delete(self, url, params=None, headers=None, name: str = None) -> PlaywrightAdapterResponse:
        # DELETE typically doesn't have a body, but Playwright allows 'data' and 'form'
        # For simplicity, this adapter's delete won't explicitly handle request bodies for DELETE
        # unless data is passed through the 'data' param by the caller.
        response = self.client.delete(url, params=params, headers=headers)
        return PlaywrightAdapterResponse(response)
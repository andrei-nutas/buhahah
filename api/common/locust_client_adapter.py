import time
import logging 
from locust.clients import HttpSession 

from api.common.client_adapters import BaseAdapter 
from api.common.response_adapter import LocustAdapterResponse, AbstractAdapterResponse

class LocustAdapter(BaseAdapter):
    def __init__(self, locust_httpuser_client: HttpSession, environment):
        self.client = locust_httpuser_client 
        self.environment = environment 

    def _fire_data_point_event(self, request_name: str, response_time: float, context: dict = None):
        can_fire = False
        reason = ""
        if not self.environment:
            reason = "self.environment is None in LocustAdapter"
        elif not hasattr(self.environment.events, 'custom_request_data_point'):
            reason = "'custom_request_data_point' event hook not found on self.environment.events"
        else:
            can_fire = True

        if can_fire:
            user_count = self.environment.runner.user_count if self.environment.runner else 0
            logging.debug(f"LocustAdapter: Firing 'custom_request_data_point' for '{request_name}' with user_count: {user_count}, response_time: {response_time:.2f}ms")
            self.environment.events.custom_request_data_point.fire(
                request_name=request_name,
                response_time=response_time,
                user_count=user_count,
                context=context or {}
            )
        else:
            logging.warning(f"LocustAdapter: Could NOT fire 'custom_request_data_point' for '{request_name}'. Reason: {reason}")

    def get(self, url, params=None, headers=None, name: str = None) -> LocustAdapterResponse:
        locust_name = name if name else url 
        start_time = time.time()
        response = self.client.get(url, params=params, headers=headers, name=locust_name)
        response_time_ms = (time.time() - start_time) * 1000
        if name: 
            self._fire_data_point_event(locust_name, response_time_ms)
        return LocustAdapterResponse(response)

    def post(self, url, data=None, json=None, params=None, headers=None, multipart=None, name: str = None) -> LocustAdapterResponse:
        locust_name = name if name else url
        start_time = time.time()

        if multipart:
            # 1) Extract the "data" part (the JSON metadata) into a form‐field
            form_data = { "data": multipart.get("data") }

            # 2) Extract the "file" part into files= for requests
            files = {}
            file_info = multipart.get("file")
            if isinstance(file_info, dict) and "name" in file_info and "buffer" in file_info:
                files["file"] = (
                    file_info["name"],
                    file_info["buffer"],
                    file_info.get("mimeType")
                )
            else:
                logging.warning(f"LocustAdapter: malformed 'file' part in multipart: {file_info!r}")

            response = self.client.post(
                url,
                data=form_data,
                params=params,
                headers=headers,
                files=files,
                name=locust_name
            )
        else:
            # Fallback to the normal data/json path
            response = self.client.post(
                url,
                data=data,
                json=json,
                params=params,
                headers=headers,
                name=locust_name
            )

        response_time_ms = (time.time() - start_time) * 1000
        if name:
            self._fire_data_point_event(locust_name, response_time_ms)
        return LocustAdapterResponse(response)

    def patch(self, url, data=None, json=None, params=None, headers=None, name: str = None) -> LocustAdapterResponse:
        locust_name = name if name else url
        start_time = time.time()
        response = self.client.patch(url, data=data, json=json, params=params, headers=headers, name=locust_name)
        response_time_ms = (time.time() - start_time) * 1000
        if name:
            self._fire_data_point_event(locust_name, response_time_ms)
        return LocustAdapterResponse(response)

    def delete(self, url, params=None, headers=None, name: str = None) -> LocustAdapterResponse:
        locust_name = name if name else url
        start_time = time.time()
        response = self.client.delete(url, params=params, headers=headers, name=locust_name)
        response_time_ms = (time.time() - start_time) * 1000
        if name:
             self._fire_data_point_event(locust_name, response_time_ms)
        return LocustAdapterResponse(response)
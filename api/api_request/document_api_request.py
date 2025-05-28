from playwright.sync_api import APIRequestContext

from api.api_request.endpoints import Endpoint

class DocumentApi:

    def __init__(self, request_context: APIRequestContext):
        self.request_context = request_context

    def get_document_by_id_response(self, document_id: str):
        response = self.get_document_by_id(document_id)
        assert response.ok, f"API request failed: {response.json()}"
        return response.json()

    def get_document_by_id(self, document_id: str):
        return self.request_context.get(url = Endpoint.get("document_id", paths = {"document_id": document_id}))

    def patch_document_response(self, document_id: str):
        response = self.request_context.patch(url = Endpoint.get("document_id", paths = {"document_id": document_id}))
        assert response.ok, f"API request failed: {response.json()}"
        return response.json()

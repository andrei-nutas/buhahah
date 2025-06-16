from api.common.client_adapters import BaseAdapter
from api.common.response_adapter import AbstractAdapterResponse
from api.endpoints import Endpoint

class DocumentApi:
    def __init__(self, adapter: BaseAdapter):
        self.adapter = adapter

    def get_document_by_id_raw(self, document_id: str) -> AbstractAdapterResponse:
        """Returns the AbstractAdapterResponse for advanced assertions or direct access."""
        return self.adapter.get(url=Endpoint.get("document_id", paths={"document_id": document_id}))

    def get_document_by_id_response(self, document_id: str) -> dict:
        """Gets document by ID, asserts response is OK, and returns JSON."""
        response = self.get_document_by_id_raw(document_id)
        assert response.ok, f"API request failed: {response.status_code} - {response.text()}"
        return response.json()

    def patch_document_raw(self, document_id: str, payload: dict = None) -> AbstractAdapterResponse:
        """Patches document, returns the AbstractAdapterResponse."""
        return self.adapter.patch(url=Endpoint.get("document_id", paths={"document_id": document_id}), json=payload)

    def patch_document_response(self, document_id: str, payload: dict = None) -> dict:
        """Patches document, asserts response is OK, and returns JSON."""
        response = self.patch_document_raw(document_id, payload=payload)
        assert response.ok, f"API request failed: {response.status_code} - {response.text()}"
        return response.json()
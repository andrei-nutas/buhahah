class Endpoint:
    path = {
        #project
        "project": "project",
        "project_id": "project/{project_id}",
        "project_mine": "project/mine",
        #document
        "project_document": "project/{project_id}/document",
        "project_document_id": "project/{project_id}/document/{document_id}",
        "document_start_processing": "project/{project_id}/document/start-processing",
        "document_id": "document/{document_id}",
        "document_download": "document/{document_id}/download",
        #overview
        "overview": "overview/{project_id}",
        "overview_confirm": "overview/{project_id}/confirm",
        #requierments
        "requierments": "requierments/project_id",
        "requirements_confirm": "requirements/{project_id}/confirm",
        #epics
        "epics": "epics/{project_id}",
        "epics_confirm": "epics/{project_id}/confirm",
        #stories
        "stories": "stories/{project_id}",
        #user
        "current_user_profile": "authorize",
        "logout": "logout",
        "users": "users",
        #jira
        "export_csv": "projects/{project_id}/export/csv",
        "jira_auth": "jira/auth",
        "export_jira": "projects/{project_id}/export/jira",
        #other
        "chat": "project/{project_id}/chat/generate",
        "health": "health"
    }

    @classmethod
    def get(cls, key, paths = None):
        try:
            endpoint = cls.path[key]
            if paths:
                endpoint = endpoint.format(**paths)
            return endpoint
        except KeyError as e:
            raise ValueError(f"Missing required URL parameter: {e}") from e
        except Exception as e:
            raise ValueError(f"Failed to build endpoint for '{key}': {e}") from e

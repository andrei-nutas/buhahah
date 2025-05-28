class Endpoint:
    path = {
        "project": "project",
        "project_archived": "project/archived",
        "project_id": "project/{project_id}",
        "project_events": "project/{project_id}/events",
        "project_team": "project/{project_id}/team",
        "project_owner": "project/{project_id}/owner",
        "project_document": "project/{project_id}/document",
        "project_document_id": "project/{project_id}/document/{document_id}",
        "project_section_id": "project/{project_id}/section/{section_id}",
        "project_section_id_status": "project/{project_id}/section/{section_id}/status",
        "project_section_id_assign": "project/{project_id}/section/{section_id}/assign",
        "project_process_rfp": "project/{project_id}/process-rfp",
        "project_storyline_structure": "project/{project_id}/storyline-structure",
        "project_generate_content": "project/{project_id}/content-generation",
        "document_id": "document/{document_id}",
        "my_project": "me/project",
        "my_project_assigned": "me/project/assigned",
        "my_project_id": "me/project/{project_id}",
        "current_user_profile": "authorize",
        "logout": "logout",
        "users": "users",
        "notifications": "me/notifications",
        "notification_events": "me/notifications/events",
        "notification_read": "me/notifications/{notification_id}/read",
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

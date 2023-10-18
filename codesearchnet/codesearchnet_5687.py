def _credentials_from_request(request):
    """Gets the authorized credentials for this flow, if they exist."""
    # ORM storage requires a logged in user
    if (oauth2_settings.storage_model is None or
            request.user.is_authenticated()):
        return get_storage(request).get()
    else:
        return None
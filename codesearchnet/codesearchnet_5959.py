def get_creds_from_kwargs(kwargs):
    """Helper to get creds out of kwargs."""
    creds = {
        'key_file': kwargs.pop('key_file', None),
        'http_auth': kwargs.pop('http_auth', None),
        'project': kwargs.get('project', None),
        'user_agent': kwargs.pop('user_agent', None),
        'api_version': kwargs.pop('api_version', 'v1')
    }
    return (creds, kwargs)
def search_projects(session,
                    query,
                    search_filter=None,
                    project_details=None,
                    user_details=None,
                    limit=10,
                    offset=0,
                    active_only=None):
    """
    Search for all projects
    """
    search_data = {
        'query': query,
        'limit': limit,
        'offset': offset,
    }
    if search_filter:
        search_data.update(search_filter)
    if project_details:
        search_data.update(project_details)
    if user_details:
        search_data.update(user_details)

    # GET /api/projects/0.1/projects/all/
    # GET /api/projects/0.1/projects/active/
    endpoint = 'projects/{}'.format('active' if active_only else 'all')
    response = make_get_request(session, endpoint, params_data=search_data)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['result']
    else:
        raise ProjectsNotFoundException(
            message=json_data['message'],
            error_code=json_data['error_code'],
            request_id=json_data['request_id'])
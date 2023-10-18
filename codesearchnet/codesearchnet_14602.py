def get_projects(session, query):
    """
    Get one or more projects
    """
    # GET /api/projects/0.1/projects
    response = make_get_request(session, 'projects', params_data=query)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['result']
    else:
        raise ProjectsNotFoundException(
            message=json_data['message'],
            error_code=json_data['error_code'],
            request_id=json_data['request_id'])
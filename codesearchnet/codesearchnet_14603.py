def get_project_by_id(session, project_id, project_details=None, user_details=None):
    """
    Get a single project by ID
    """
    # GET /api/projects/0.1/projects/<int:project_id>
    query = {}
    if project_details:
        query.update(project_details)
    if user_details:
        query.update(user_details)
    response = make_get_request(
        session, 'projects/{}'.format(project_id), params_data=query)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['result']
    else:
        raise ProjectsNotFoundException(
            message=json_data['message'],
            error_code=json_data['error_code'],
            request_id=json_data['request_id']
        )
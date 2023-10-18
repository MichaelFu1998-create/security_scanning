def get_milestones(session, project_ids=[], milestone_ids=[], user_details=None, limit=10, offset=0):
    """
    Get the list of milestones
    """
    get_milestones_data = {}
    if milestone_ids:
        get_milestones_data['milestones[]'] = milestone_ids
    if project_ids:
        get_milestones_data['projects[]'] = project_ids
    get_milestones_data['limit'] = limit
    get_milestones_data['offset'] = offset

    # Add projections if they exist
    if user_details:
        get_milestones_data.update(user_details)

    # GET /api/projects/0.1/milestones/

    response = make_get_request(
        session, 'milestones', params_data=get_milestones_data)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['result']
    else:
        raise MilestonesNotFoundException(
            message=json_data['message'],
            error_code=json_data['error_code'],
            request_id=json_data['request_id']
        )
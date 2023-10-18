def get_milestone_by_id(session, milestone_id, user_details=None):
    """
    Get a specific milestone
    """
    # GET /api/projects/0.1/milestones/{milestone_id}/
    endpoint = 'milestones/{}'.format(milestone_id)

    response = make_get_request(session, endpoint, params_data=user_details)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['result']
    else:
        raise MilestonesNotFoundException(
            message=json_data['message'],
            error_code=json_data['error_code'],
            request_id=json_data['request_id']
        )
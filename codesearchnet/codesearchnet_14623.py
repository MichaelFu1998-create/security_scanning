def reject_milestone_request(session, milestone_request_id):
    """
    Reject a milestone request
    """
    params_data = {
        'action': 'reject',
    }
    # POST /api/projects/0.1/milestone_requests/{milestone_request_id}/?action=
    # reject
    endpoint = 'milestone_requests/{}'.format(milestone_request_id)
    response = make_put_request(session, endpoint, params_data=params_data)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['status']
    else:
        raise MilestoneRequestNotRejectedException(
            message=json_data['message'],
            error_code=json_data['error_code'],
            request_id=json_data['request_id'])
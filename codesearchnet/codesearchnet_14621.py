def create_milestone_request(session, project_id, bid_id, description, amount):
    """
    Create a milestone request
    """
    milestone_request_data = {
        'project_id': project_id,
        'bid_id': bid_id,
        'description': description,
        'amount': amount,
    }
    # POST /api/projects/0.1/milestone_requests/
    response = make_post_request(session, 'milestone_requests',
                                 json_data=milestone_request_data)
    json_data = response.json()
    if response.status_code == 200:
        milestone_request_data = json_data['result']
        return MilestoneRequest(milestone_request_data)
    else:
        raise MilestoneRequestNotCreatedException(
            message=json_data['message'],
            error_code=json_data['error_code'],
            request_id=json_data['request_id'])
def create_milestone_payment(session, project_id, bidder_id, amount,
                             reason, description):
    """
    Create a milestone payment
    """
    milestone_data = {
        'project_id': project_id,
        'bidder_id': bidder_id,
        'amount': amount,
        'reason': reason,
        'description': description
    }
    # POST /api/projects/0.1/milestones/
    response = make_post_request(session, 'milestones',
                                 json_data=milestone_data)
    json_data = response.json()
    if response.status_code == 200:
        milestone_data = json_data['result']
        return Milestone(milestone_data)
    else:
        raise MilestoneNotCreatedException(message=json_data['message'],
                                           error_code=json_data['error_code'],
                                           request_id=json_data['request_id'])
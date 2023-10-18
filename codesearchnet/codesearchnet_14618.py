def release_milestone_payment(session, milestone_id, amount):
    """
    Release a milestone payment
    """
    params_data = {
        'action': 'release',
    }
    milestone_data = {
        'amount': amount,
    }
    # PUT /api/projects/0.1/milestones/{milestone_id}/?action=release
    endpoint = 'milestones/{}'.format(milestone_id)
    response = make_put_request(session, endpoint, params_data=params_data,
                                json_data=milestone_data)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['status']
    else:
        raise MilestoneNotReleasedException(message=json_data['message'],
                                            error_code=json_data['error_code'],
                                            request_id=json_data['request_id'])
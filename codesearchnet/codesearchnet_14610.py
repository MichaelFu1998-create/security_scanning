def revoke_project_bid(session, bid_id):
    """
    Revoke a bid on a project
    """
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    bid_data = {
        'action': 'revoke'
    }
    # POST /api/projects/0.1/bids/{bid_id}/?action=revoke
    endpoint = 'bids/{}'.format(bid_id)
    response = make_put_request(session, endpoint, headers=headers,
                                params_data=bid_data)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['status']
    else:
        json_data = response.json()
        raise BidNotRevokedException(message=json_data['message'],
                                     error_code=json_data['error_code'],
                                     request_id=json_data['request_id'])
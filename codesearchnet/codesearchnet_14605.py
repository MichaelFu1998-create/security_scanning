def place_project_bid(session, project_id, bidder_id, description, amount,
                      period, milestone_percentage):
    """
    Place a bid on a project
    """
    bid_data = {
        'project_id': project_id,
        'bidder_id': bidder_id,
        'description': description,
        'amount': amount,
        'period': period,
        'milestone_percentage': milestone_percentage,
    }
    # POST /api/projects/0.1/bids/
    response = make_post_request(session, 'bids', json_data=bid_data)
    json_data = response.json()
    if response.status_code == 200:
        bid_data = json_data['result']
        return Bid(bid_data)
    else:
        raise BidNotPlacedException(message=json_data['message'],
                                    error_code=json_data['error_code'],
                                    request_id=json_data['request_id'])
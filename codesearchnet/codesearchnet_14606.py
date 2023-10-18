def get_bids(session, project_ids=[], bid_ids=[], limit=10, offset=0):
    """
    Get the list of bids
    """
    get_bids_data = {}
    if bid_ids:
        get_bids_data['bids[]'] = bid_ids
    if project_ids:
        get_bids_data['projects[]'] = project_ids
    get_bids_data['limit'] = limit
    get_bids_data['offset'] = offset
    # GET /api/projects/0.1/bids/
    response = make_get_request(session, 'bids', params_data=get_bids_data)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['result']
    else:
        raise BidsNotFoundException(
            message=json_data['message'], error_code=json_data['error_code'],
            request_id=json_data['request_id']
        )
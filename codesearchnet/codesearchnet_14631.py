def get_messages(session, query, limit=10, offset=0):
    """
    Get one or more messages
    """
    query['limit'] = limit
    query['offset'] = offset

    # GET /api/messages/0.1/messages
    response = make_get_request(session, 'messages', params_data=query)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['result']
    else:
        raise MessagesNotFoundException(
            message=json_data['message'],
            error_code=json_data['error_code'],
            request_id=json_data['request_id']
        )
def search_messages(session, thread_id, query, limit=20,
                    offset=0, message_context_details=None,
                    window_above=None, window_below=None):
    """
    Search for messages
    """
    query = {
        'thread_id': thread_id,
        'query': query,
        'limit': limit,
        'offset': offset
    }
    if message_context_details:
        query['message_context_details'] = message_context_details
    if window_above:
        query['window_above'] = window_above
    if window_below:
        query['window_below'] = window_below

    # GET /api/messages/0.1/messages/search
    response = make_get_request(session, 'messages/search', params_data=query)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['result']
    else:
        raise MessagesNotFoundException(
            message=json_data['message'],
            error_code=json_data['error_code'],
            request_id=json_data['request_id']
        )
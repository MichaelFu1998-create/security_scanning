def get_threads(session, query):
    """
    Get one or more threads
    """
    # GET /api/messages/0.1/threads
    response = make_get_request(session, 'threads', params_data=query)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['result']
    else:
        raise ThreadsNotFoundException(
            message=json_data['message'],
            error_code=json_data['error_code'],
            request_id=json_data['request_id']
        )
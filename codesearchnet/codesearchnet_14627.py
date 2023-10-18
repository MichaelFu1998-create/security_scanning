def create_thread(session, member_ids, context_type, context, message):
    """
    Create a thread
    """
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    thread_data = {
        'members[]': member_ids,
        'context_type': context_type,
        'context': context,
        'message': message,
    }

    # POST /api/messages/0.1/threads/
    response = make_post_request(session, 'threads', headers,
                                 form_data=thread_data)
    json_data = response.json()
    if response.status_code == 200:
        return Thread(json_data['result'])
    else:
        raise ThreadNotCreatedException(message=json_data['message'],
                                        error_code=json_data['error_code'],
                                        request_id=json_data['request_id'])
def post_message(session, thread_id, message):
    """
    Add a message to a thread
    """
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    message_data = {
        'message': message,
    }

    # POST /api/messages/0.1/threads/{thread_id}/messages/
    endpoint = 'threads/{}/messages'.format(thread_id)
    response = make_post_request(session, endpoint, headers,
                                 form_data=message_data)
    json_data = response.json()
    if response.status_code == 200:
        return Message(json_data['result'])
    else:
        raise MessageNotCreatedException(message=json_data['message'],
                                         error_code=json_data['error_code'],
                                         request_id=json_data['request_id'])
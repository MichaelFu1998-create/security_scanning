def post_attachment(session, thread_id, attachments):
    """
    Add a message to a thread
    """
    files = []
    filenames = []
    for attachment in attachments:
        files.append(attachment['file'])
        filenames.append(attachment['filename'])
    message_data = {
        'attachments[]': filenames,
    }

    # POST /api/messages/0.1/threads/{thread_id}/messages/
    endpoint = 'threads/{}/messages'.format(thread_id)
    response = make_post_request(session, endpoint,
                                 form_data=message_data, files=files)
    json_data = response.json()
    if response.status_code == 200:
        return Message(json_data['result'])
    else:
        raise MessageNotCreatedException(message=json_data['message'],
                                         error_code=json_data['error_code'],
                                         request_id=json_data['request_id'])
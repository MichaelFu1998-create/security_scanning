def get_self(session, user_details=None):
    """
    Get details about the currently authenticated user
    """
    # Set compact to true
    if user_details:
        user_details['compact'] = True
    response = make_get_request(session, 'self', params_data=user_details)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['result']
    else:
        raise SelfNotRetrievedException(
            message=json_data['message'],
            error_code=json_data['error_code'],
            request_id=json_data['request_id']
        )
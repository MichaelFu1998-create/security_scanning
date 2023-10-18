def get_user_by_id(session, user_id, user_details=None):
    """
    Get details about specific user
    """
    if user_details:
        user_details['compact'] = True
    response = make_get_request(
        session, 'users/{}'.format(user_id), params_data=user_details)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['result']
    else:
        raise UserNotFoundException(
            message=json_data['message'],
            error_code=json_data['error_code'],
            request_id=json_data['request_id']
        )
def get_users(session, query):
    """
    Get one or more users
    """
    # GET /api/users/0.1/users
    response = make_get_request(session, 'users', params_data=query)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['result']
    else:
        raise UsersNotFoundException(
            message=json_data['message'],
            error_code=json_data['error_code'],
            request_id=json_data['request_id'])
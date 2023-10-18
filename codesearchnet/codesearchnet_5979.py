def get_group(group_name, users=True, client=None, **kwargs):
    """Get's the IAM Group details.

    :param group_name:
    :param users: Optional -- will return the IAM users that the group is attached to if desired (paginated).
    :param client:
    :param kwargs:
    :return:
    """
    # First, make the initial call to get the details for the group:
    result = client.get_group(GroupName=group_name, **kwargs)

    # If we care about the user details, then fetch them:
    if users:
        if result.get('IsTruncated'):
            kwargs_to_send = {'GroupName': group_name}
            kwargs_to_send.update(kwargs)

            user_list = result['Users']
            kwargs_to_send['Marker'] = result['Marker']

            result['Users'] = user_list + _get_users_for_group(client, **kwargs_to_send)

    else:
        result.pop('Users', None)
        result.pop('IsTruncated', None)
        result.pop('Marker', None)

    return result
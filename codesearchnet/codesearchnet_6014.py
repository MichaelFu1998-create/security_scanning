def get_users(group, **conn):
    """Gets a list of the usernames that are a part of this group."""
    group_details = get_group_api(group['GroupName'], **conn)

    user_list = []
    for user in group_details.get('Users', []):
        user_list.append(user['UserName'])

    return user_list
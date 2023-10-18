def get_all_users(flags=FLAGS.ACCESS_KEYS | FLAGS.MFA_DEVICES | FLAGS.LOGIN_PROFILE | FLAGS.SIGNING_CERTIFICATES,
                  **conn):
    """
    Returns a list of Users represented as dictionary below:

    {
        "Arn": ...,
        "AccessKeys": ...,
        "CreateDate": ...,  # str
        "InlinePolicies": ...,
        "ManagedPolicies": ...,
        "MFADevices": ...,
        "Path": ...,
        "UserId": ...,
        "UserName": ...,
        "SigningCerts": ...
    }

    :param flags:
    :param conn: dict containing enough information to make a connection to the desired account.
    :return: list of dicts containing fully built out user.
    """

    users = []
    account_users = get_account_authorization_details('User', **conn)

    for user in account_users:
        temp_user = {
            'Arn': user['Arn'],
            'CreateDate': get_iso_string(user['CreateDate']),
            'GroupList': user['GroupList'],
            'InlinePolicies': user['UserPolicyList'],
            'ManagedPolicies': [
                {
                  "name": x['PolicyName'],
                  "arn": x['PolicyArn']
                } for x in user['AttachedManagedPolicies']
            ],
            'Path': user['Path'],
            'UserId': user['UserId'],
            'UserName': user['UserName']
        }

        user = modify(temp_user, output='camelized')
        _conn_from_args(user, conn)
        users.append(registry.build_out(flags, start_with=user, pass_datastructure=True, **conn))

    return users
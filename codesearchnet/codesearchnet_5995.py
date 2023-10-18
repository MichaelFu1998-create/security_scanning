def get_all_roles(**conn):
    """
    Returns a List of Roles represented as the dictionary below:

    {
        "Arn": ...,
        "AssumeRolePolicyDocument": ...,
        "CreateDate": ...,  # str
        "InlinePolicies": ...,
        "InstanceProfiles": ...,
        "ManagedPolicies": ...,
        "Path": ...,
        "RoleId": ...,
        "RoleName": ...,
    }

    :param conn: dict containing enough information to make a connection to the desired account.
    :return: list containing dicts or fully built out roles
    """

    roles = []
    account_roles = get_account_authorization_details('Role', **conn)

    for role in account_roles:
        roles.append(
            {
                'Arn': role['Arn'],
                'AssumeRolePolicyDocument': role['AssumeRolePolicyDocument'],
                'CreateDate': get_iso_string(role['CreateDate']),
                'InlinePolicies': role['RolePolicyList'],
                'InstanceProfiles': [{
                                        'path': ip['Path'],
                                        'instance_profile_name': ip['InstanceProfileName'],
                                        'create_date': get_iso_string(ip['CreateDate']),
                                        'instance_profile_id': ip['InstanceProfileId'],
                                        'arn': ip['Arn']
                                    } for ip in role['InstanceProfileList']],
                'ManagedPolicies': [
                    {
                      "name": x['PolicyName'],
                      "arn": x['PolicyArn']
                    } for x in role['AttachedManagedPolicies']
                ],
                'Path': role['Path'],
                'RoleId': role['RoleId'],
                'RoleName': role['RoleName']
            }
        )

    return roles
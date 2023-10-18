def get_group(group, flags=FLAGS.BASE | FLAGS.INLINE_POLICIES | FLAGS.MANAGED_POLICIES, **conn):
    """
    Orchestrates all the calls required to fully build out an IAM Group in the following format:

    {
        "Arn": ...,
        "GroupName": ...,
        "Path": ...,
        "GroupId": ...,
        "CreateDate": ...,  # str
        "InlinePolicies": ...,
        "ManagedPolicies": ...,  # These are just the names of the Managed Policies.
        "Users": ...,  # False by default -- these are just the names of the users.
        "_version": 1
    }

    :param flags: By default, Users is disabled. This is somewhat expensive as it has to call the `get_group` call
                  multiple times.
    :param group: dict MUST contain the GroupName and also a combination of either the ARN or the account_number.
    :param output: Determines whether keys should be returned camelized or underscored.
    :param conn: dict containing enough information to make a connection to the desired account.
                 Must at least have 'assume_role' key.
    :return: dict containing fully built out Group.
    """
    if not group.get('GroupName'):
        raise MissingFieldException('Must include GroupName.')

    group = modify(group, output='camelized')
    _conn_from_args(group, conn)
    return registry.build_out(flags, start_with=group, pass_datastructure=True, **conn)
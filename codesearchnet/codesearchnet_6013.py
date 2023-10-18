def get_managed_policies(group, **conn):
    """Get a list of the managed policy names that are attached to the group."""
    managed_policies = list_attached_group_managed_policies(group['GroupName'], **conn)

    managed_policy_names = []

    for policy in managed_policies:
        managed_policy_names.append(policy['PolicyName'])

    return managed_policy_names
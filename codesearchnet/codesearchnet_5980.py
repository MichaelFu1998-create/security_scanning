def get_group_policy_document(group_name, policy_name, client=None, **kwargs):
    """Fetches the specific IAM group inline-policy document."""
    return client.get_group_policy(GroupName=group_name, PolicyName=policy_name, **kwargs)['PolicyDocument']
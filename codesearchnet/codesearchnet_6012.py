def get_inline_policies(group, **conn):
    """Get the inline policies for the group."""
    policy_list = list_group_policies(group['GroupName'])

    policy_documents = {}

    for policy in policy_list:
        policy_documents[policy] = get_group_policy_document(group['GroupName'], policy, **conn)

    return policy_documents
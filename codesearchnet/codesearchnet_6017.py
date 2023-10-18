def get_base(managed_policy, **conn):
    """Fetch the base Managed Policy.

    This includes the base policy and the latest version document.

    :param managed_policy:
    :param conn:
    :return:
    """
    managed_policy['_version'] = 1

    arn = _get_name_from_structure(managed_policy, 'Arn')
    policy = get_policy(arn, **conn)
    document = get_managed_policy_document(arn, policy_metadata=policy, **conn)

    managed_policy.update(policy['Policy'])
    managed_policy['Document'] = document

    # Fix the dates:
    managed_policy['CreateDate'] = get_iso_string(managed_policy['CreateDate'])
    managed_policy['UpdateDate'] = get_iso_string(managed_policy['UpdateDate'])

    return managed_policy
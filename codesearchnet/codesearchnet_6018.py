def get_managed_policy(managed_policy, flags=FLAGS.ALL, **conn):
    """
    Orchestrates all of the calls required to fully build out an IAM Managed Policy in the following format:

    {
        "Arn": "...",
        "PolicyName": "...",
        "PolicyId": "...",
        "Path": "...",
        "DefaultVersionId": "...",
        "AttachmentCount": 123,
        "PermissionsBoundaryUsageCount": 123,
        "IsAttachable": ...,
        "Description": "...",
        "CreateDate": "...",
        "UpdateDate": "...",
        "Document": "...",
        "_version": 1
    }

    :param managed_policy: dict MUST contain the ARN.
    :param flags:
    :param conn:
    :return:
    """
    _conn_from_args(managed_policy, conn)
    return registry.build_out(flags, start_with=managed_policy, pass_datastructure=True, **conn)
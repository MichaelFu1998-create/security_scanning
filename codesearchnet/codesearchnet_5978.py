def get_managed_policy_document(policy_arn, policy_metadata=None, client=None, **kwargs):
    """Retrieve the currently active (i.e. 'default') policy version document for a policy.

    :param policy_arn:
    :param policy_metadata: This is a previously fetch managed policy response from boto/cloudaux.
                            This is used to prevent unnecessary API calls to get the initial policy default version id.
    :param client:
    :param kwargs:
    :return:
    """
    if not policy_metadata:
        policy_metadata = client.get_policy(PolicyArn=policy_arn)

    policy_document = client.get_policy_version(PolicyArn=policy_arn,
                                                VersionId=policy_metadata['Policy']['DefaultVersionId'])
    return policy_document['PolicyVersion']['Document']
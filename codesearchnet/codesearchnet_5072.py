def get_account_id(
    profile_name, aws_access_key_id, aws_secret_access_key,
    region=None,
):
    """Query STS for a users' account_id"""
    client = get_client(
        'sts', profile_name, aws_access_key_id, aws_secret_access_key,
        region,
    )
    return client.get_caller_identity().get('Account')
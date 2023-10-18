def get_client(
    client, profile_name, aws_access_key_id, aws_secret_access_key,
    region=None,
):
    """Shortcut for getting an initialized instance of the boto3 client."""

    boto3.setup_default_session(
        profile_name=profile_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region,
    )
    return boto3.client(client)
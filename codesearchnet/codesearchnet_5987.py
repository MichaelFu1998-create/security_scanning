def sts_conn(service, service_type='client', future_expiration_minutes=15):
    """
    This will wrap all calls with an STS AssumeRole if the required parameters are sent over.
    Namely, it requires the following in the kwargs:
    - Service Type (Required)
    - Account Number (Required for Assume Role)
    - IAM Role Name (Required for Assume Role)
    - Region (Optional, but recommended)
    - AWS Partition (Optional, defaults to 'aws' if none specified)
    - IAM Session Name (Optional, but recommended to appear in CloudTrail)

    If `force_client` is set to a boto3 client, then this will simply pass that in as the client.
    `force_client` is mostly useful for mocks and tests.
    :param service:
    :param service_type:
    :param future_expiration_minutes:
    :return:
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if kwargs.get("force_client"):
                kwargs[service_type] = kwargs.pop("force_client")
                kwargs.pop("account_number", None)
                kwargs.pop("region", None)
            else:
                kwargs[service_type] = boto3_cached_conn(
                    service,
                    service_type=service_type,
                    future_expiration_minutes=future_expiration_minutes,
                    account_number=kwargs.pop('account_number', None),
                    assume_role=kwargs.pop('assume_role', None),
                    session_name=kwargs.pop('session_name', 'cloudaux'),
                    external_id=kwargs.pop('external_id', None),
                    region=kwargs.pop('region', 'us-east-1'),
                    arn_partition=kwargs.pop('arn_partition', 'aws')
                )
            return f(*args, **kwargs)
        return decorated_function
    return decorator
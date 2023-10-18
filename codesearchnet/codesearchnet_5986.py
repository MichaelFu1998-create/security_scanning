def boto3_cached_conn(service, service_type='client', future_expiration_minutes=15, account_number=None,
                      assume_role=None, session_name='cloudaux', region='us-east-1', return_credentials=False,
                      external_id=None, arn_partition='aws'):
    """
    Used to obtain a boto3 client or resource connection.
    For cross account, provide both account_number and assume_role.

    :usage:

    # Same Account:
    client = boto3_cached_conn('iam')
    resource = boto3_cached_conn('iam', service_type='resource')

    # Cross Account Client:
    client = boto3_cached_conn('iam', account_number='000000000000', assume_role='role_name')

    # Cross Account Resource:
    resource = boto3_cached_conn('iam', service_type='resource', account_number='000000000000', assume_role='role_name')

    :param service: AWS service (i.e. 'iam', 'ec2', 'kms')
    :param service_type: 'client' or 'resource'
    :param future_expiration_minutes: Connections will expire from the cache
        when their expiration is within this many minutes of the present time. [Default 15]
    :param account_number: Required if assume_role is provided.
    :param assume_role:  Name of the role to assume into for account described by account_number.
    :param session_name: Session name to attach to requests. [Default 'cloudaux']
    :param region: Region name for connection. [Default us-east-1]
    :param return_credentials: Indicates if the STS credentials should be returned with the client [Default False]
    :param external_id: Optional external id to pass to sts:AssumeRole.
        See https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html
    :param arn_partition: Optional parameter to specify other aws partitions such as aws-us-gov for aws govcloud
    :return: boto3 client or resource connection
    """
    key = (
        account_number,
        assume_role,
        session_name,
        external_id,
        region,
        service_type,
        service,
        arn_partition
    )

    if key in CACHE:
        retval = _get_cached_creds(key, service, service_type, region, future_expiration_minutes, return_credentials)
        if retval:
            return retval

    role = None
    if assume_role:
        sts = boto3.session.Session().client('sts')

        # prevent malformed ARN
        if not all([account_number, assume_role]):
            raise ValueError("Account number and role to assume are both required")

        arn = 'arn:{partition}:iam::{0}:role/{1}'.format(
            account_number,
            assume_role,
            partition=arn_partition
        )

        assume_role_kwargs = {
            'RoleArn': arn,
            'RoleSessionName': session_name
        }

        if external_id:
            assume_role_kwargs['ExternalId'] = external_id

        role = sts.assume_role(**assume_role_kwargs)

    if service_type == 'client':
        conn = _client(service, region, role)
    elif service_type == 'resource':
        conn = _resource(service, region, role)

    if role:
        CACHE[key] = role

    if return_credentials:
        return conn, role['Credentials']

    return conn
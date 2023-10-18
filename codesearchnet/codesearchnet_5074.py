def create_function(cfg, path_to_zip_file, use_s3=False, s3_file=None):
    """Register and upload a function to AWS Lambda."""

    print('Creating your new Lambda function')
    byte_stream = read(path_to_zip_file, binary_file=True)
    profile_name = cfg.get('profile')
    aws_access_key_id = cfg.get('aws_access_key_id')
    aws_secret_access_key = cfg.get('aws_secret_access_key')

    account_id = get_account_id(
        profile_name, aws_access_key_id, aws_secret_access_key, cfg.get(
            'region',
        ),
    )
    role = get_role_name(
        cfg.get('region'), account_id,
        cfg.get('role', 'lambda_basic_execution'),
    )

    client = get_client(
        'lambda', profile_name, aws_access_key_id, aws_secret_access_key,
        cfg.get('region'),
    )

    # Do we prefer development variable over config?
    buck_name = (
        os.environ.get('S3_BUCKET_NAME') or cfg.get('bucket_name')
    )
    func_name = (
        os.environ.get('LAMBDA_FUNCTION_NAME') or cfg.get('function_name')
    )
    print('Creating lambda function with name: {}'.format(func_name))

    if use_s3:
        kwargs = {
            'FunctionName': func_name,
            'Runtime': cfg.get('runtime', 'python2.7'),
            'Role': role,
            'Handler': cfg.get('handler'),
            'Code': {
                'S3Bucket': '{}'.format(buck_name),
                'S3Key': '{}'.format(s3_file),
            },
            'Description': cfg.get('description', ''),
            'Timeout': cfg.get('timeout', 15),
            'MemorySize': cfg.get('memory_size', 512),
            'VpcConfig': {
                'SubnetIds': cfg.get('subnet_ids', []),
                'SecurityGroupIds': cfg.get('security_group_ids', []),
            },
            'Publish': True,
        }
    else:
        kwargs = {
            'FunctionName': func_name,
            'Runtime': cfg.get('runtime', 'python2.7'),
            'Role': role,
            'Handler': cfg.get('handler'),
            'Code': {'ZipFile': byte_stream},
            'Description': cfg.get('description', ''),
            'Timeout': cfg.get('timeout', 15),
            'MemorySize': cfg.get('memory_size', 512),
            'VpcConfig': {
                'SubnetIds': cfg.get('subnet_ids', []),
                'SecurityGroupIds': cfg.get('security_group_ids', []),
            },
            'Publish': True,
        }

    if 'tags' in cfg:
        kwargs.update(
            Tags={
                key: str(value)
                for key, value in cfg.get('tags').items()
            }
        )

    if 'environment_variables' in cfg:
        kwargs.update(
            Environment={
                'Variables': {
                    key: get_environment_variable_value(value)
                    for key, value
                    in cfg.get('environment_variables').items()
                },
            },
        )

    client.create_function(**kwargs)

    concurrency = get_concurrency(cfg)
    if concurrency > 0:
        client.put_function_concurrency(FunctionName=func_name, ReservedConcurrentExecutions=concurrency)
def update_function(
        cfg, path_to_zip_file, existing_cfg, use_s3=False, s3_file=None, preserve_vpc=False
):
    """Updates the code of an existing Lambda function"""

    print('Updating your Lambda function')
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

    if use_s3:
        client.update_function_code(
            FunctionName=cfg.get('function_name'),
            S3Bucket='{}'.format(buck_name),
            S3Key='{}'.format(s3_file),
            Publish=True,
        )
    else:
        client.update_function_code(
            FunctionName=cfg.get('function_name'),
            ZipFile=byte_stream,
            Publish=True,
        )

    kwargs = {
        'FunctionName': cfg.get('function_name'),
        'Role': role,
        'Runtime': cfg.get('runtime'),
        'Handler': cfg.get('handler'),
        'Description': cfg.get('description', ''),
        'Timeout': cfg.get('timeout', 15),
        'MemorySize': cfg.get('memory_size', 512),
    }

    if preserve_vpc:
        kwargs['VpcConfig'] = existing_cfg.get('Configuration', {}).get('VpcConfig')
        if kwargs['VpcConfig'] is None:
            kwargs['VpcConfig'] = {
                'SubnetIds': cfg.get('subnet_ids', []),
                'SecurityGroupIds': cfg.get('security_group_ids', []),
            }
        else:
            del kwargs['VpcConfig']['VpcId']
    else:
        kwargs['VpcConfig'] = {
            'SubnetIds': cfg.get('subnet_ids', []),
            'SecurityGroupIds': cfg.get('security_group_ids', []),
        }

    if 'environment_variables' in cfg:
        kwargs.update(
            Environment={
                'Variables': {
                    key: str(get_environment_variable_value(value))
                    for key, value
                    in cfg.get('environment_variables').items()
                },
            },
        )

    ret = client.update_function_configuration(**kwargs)

    concurrency = get_concurrency(cfg)
    if concurrency > 0:
        client.put_function_concurrency(FunctionName=cfg.get('function_name'), ReservedConcurrentExecutions=concurrency)
    elif 'Concurrency' in existing_cfg:
        client.delete_function_concurrency(FunctionName=cfg.get('function_name'))

    if 'tags' in cfg:
        tags = {
            key: str(value)
            for key, value in cfg.get('tags').items()
        }
        if tags != existing_cfg.get('Tags'):
            if existing_cfg.get('Tags'):
                client.untag_resource(Resource=ret['FunctionArn'],
                                      TagKeys=list(existing_cfg['Tags'].keys()))
            client.tag_resource(Resource=ret['FunctionArn'], Tags=tags)
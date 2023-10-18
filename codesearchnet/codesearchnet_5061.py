def cleanup_old_versions(
    src, keep_last_versions,
    config_file='config.yaml', profile_name=None,
):
    """Deletes old deployed versions of the function in AWS Lambda.

    Won't delete $Latest and any aliased version

    :param str src:
        The path to your Lambda ready project (folder must contain a valid
        config.yaml and handler module (e.g.: service.py).
    :param int keep_last_versions:
        The number of recent versions to keep and not delete
    """
    if keep_last_versions <= 0:
        print("Won't delete all versions. Please do this manually")
    else:
        path_to_config_file = os.path.join(src, config_file)
        cfg = read_cfg(path_to_config_file, profile_name)

        profile_name = cfg.get('profile')
        aws_access_key_id = cfg.get('aws_access_key_id')
        aws_secret_access_key = cfg.get('aws_secret_access_key')

        client = get_client(
            'lambda', profile_name, aws_access_key_id, aws_secret_access_key,
            cfg.get('region'),
        )

        response = client.list_versions_by_function(
            FunctionName=cfg.get('function_name'),
        )
        versions = response.get('Versions')
        if len(response.get('Versions')) < keep_last_versions:
            print('Nothing to delete. (Too few versions published)')
        else:
            version_numbers = [elem.get('Version') for elem in
                               versions[1:-keep_last_versions]]
            for version_number in version_numbers:
                try:
                    client.delete_function(
                        FunctionName=cfg.get('function_name'),
                        Qualifier=version_number,
                    )
                except botocore.exceptions.ClientError as e:
                    print('Skipping Version {}: {}'
                          .format(version_number, e.message))
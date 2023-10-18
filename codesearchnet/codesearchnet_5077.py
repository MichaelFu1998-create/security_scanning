def get_function_config(cfg):
    """Check whether a function exists or not and return its config"""

    function_name = cfg.get('function_name')
    profile_name = cfg.get('profile')
    aws_access_key_id = cfg.get('aws_access_key_id')
    aws_secret_access_key = cfg.get('aws_secret_access_key')
    client = get_client(
        'lambda', profile_name, aws_access_key_id, aws_secret_access_key,
        cfg.get('region'),
    )

    try:
        return client.get_function(FunctionName=function_name)
    except client.exceptions.ResourceNotFoundException as e:
        if 'Function not found' in str(e):
            return False
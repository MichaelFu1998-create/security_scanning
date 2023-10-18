def get_lambda_function(lambda_function, flags=FLAGS.ALL, **conn):
    """Fully describes a lambda function.
    
    Args:
        lambda_function: Name, ARN, or dictionary of lambda function. If dictionary, should likely be the return value from list_functions. At a minimum, must contain a key titled 'FunctionName'.
        flags: Flags describing which sections should be included in the return value. Default ALL
    
    Returns:
        dictionary describing the requested lambda function.
    """
    # Python 2 and 3 support:
    try:
        basestring
    except NameError as _:
        basestring = str

    # If STR is passed in, determine if it's a name or ARN and built a dict.
    if isinstance(lambda_function, basestring):
        lambda_function_arn = ARN(lambda_function)
        if lambda_function_arn.error:
            lambda_function = dict(FunctionName=lambda_function)
        else:
            lambda_function = dict(FunctionName=lambda_function_arn.name, FunctionArn=lambda_function)

    # If an ARN is available, override the account_number/region from the conn dict.
    if 'FunctionArn' in lambda_function:
        lambda_function_arn = ARN(lambda_function['FunctionArn'])
        if not lambda_function_arn.error:
            if lambda_function_arn.account_number:
                conn['account_number'] = lambda_function_arn.account_number
            if lambda_function_arn.region:
                conn['region'] = lambda_function_arn.region

    return registry.build_out(flags, start_with=lambda_function, pass_datastructure=True, **conn)
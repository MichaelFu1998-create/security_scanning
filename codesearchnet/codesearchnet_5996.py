def _get_policy(lambda_function, **conn):
    """Get LambdaFunction Policies.  (there can be many of these!)
    
    Lambda Function Policies are overly complicated.  They can be attached to a label,
    a version, and there is also a default policy.
    
    This method attempts to gather all three types.
    
    AWS returns an exception if the policy requested does not exist.  We catch and ignore these exceptions.
    """
    policies = dict(Versions=dict(), Aliases=dict(), DEFAULT=dict())

    for version in [v['Version'] for v in lambda_function['versions']]:
        try:
            policies['Versions'][version] = get_policy(FunctionName=lambda_function['FunctionName'], Qualifier=version, **conn)
            policies['Versions'][version] = json.loads(policies['Versions'][version])
        except Exception as e:
            pass

    for alias in [v['Name'] for v in lambda_function['aliases']]:
        try:
            policies['Aliases'][alias] = get_policy(FunctionName=lambda_function['FunctionName'], Qualifier=alias, **conn)
            policies['Aliases'][alias] = json.loads(policies['Aliases'][alias])
        except Exception as e:
            pass

    try:
        policies['DEFAULT'] = get_policy(FunctionName=lambda_function['FunctionName'], **conn)
        policies['DEFAULT'] = json.loads(policies['DEFAULT'])
    except Exception as e:
        pass

    return policies
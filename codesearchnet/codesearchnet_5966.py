def get_elbv2(alb, flags=FLAGS.ALL, **conn):
    """
    Fully describes an ALB (ELBv2).

    :param alb: Could be an ALB Name, ALB ARN, or a dictionary. Likely the return value from a previous call to describe_load_balancers. At a minimum, must contain a key titled 'LoadBalancerArn'.
    :param flags: Flags describing which sections should be included in the return value. Default is FLAGS.ALL.
    :return: Returns a dictionary describing the ALB with the fields described in the flags parameter.
    """
    # Python 2 and 3 support:
    try:
        basestring
    except NameError as _:
        basestring = str

    if isinstance(alb, basestring):
        from cloudaux.orchestration.aws.arn import ARN
        alb_arn = ARN(alb)
        if alb_arn.error:
            alb = dict(LoadBalancerName=alb)
        else:
            alb = dict(LoadBalancerArn=alb)

    return registry.build_out(flags, start_with=alb, pass_datastructure=True, **conn)
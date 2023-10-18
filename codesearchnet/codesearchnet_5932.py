def get_load_balancer(load_balancer, flags=FLAGS.ALL ^ FLAGS.POLICY_TYPES, **conn):
    """
    Fully describes an ELB.

    :param loadbalancer: Could be an ELB Name or a dictionary. Likely the return value from a previous call to describe_load_balancers. At a minimum, must contain a key titled 'LoadBalancerName'.
    :param flags: Flags describing which sections should be included in the return value. Default is FLAGS.ALL minus FLAGS.POLICY_TYPES.
    :return: Returns a dictionary describing the ELB with the fields described in the flags parameter.
    """
    # Python 2 and 3 support:
    try:
        basestring
    except NameError as _:
        basestring = str

    if isinstance(load_balancer, basestring):
        load_balancer = dict(LoadBalancerName=load_balancer)

    return registry.build_out(flags, start_with=load_balancer, pass_datastructure=True, **conn)
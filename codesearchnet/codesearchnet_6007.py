def describe_load_balancers(arns=None, names=None, client=None):
    """
    Permission: elasticloadbalancing:DescribeLoadBalancers
    """
    kwargs = dict()
    if arns:
        kwargs.update(dict(LoadBalancerArns=arns))
    if names:
        kwargs.update(dict(Names=names))
    return client.describe_load_balancers(**kwargs)
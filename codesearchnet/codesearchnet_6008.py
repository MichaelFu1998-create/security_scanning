def describe_listeners(load_balancer_arn=None, listener_arns=None, client=None):
    """
    Permission: elasticloadbalancing:DescribeListeners
    """
    kwargs = dict()
    if load_balancer_arn:
        kwargs.update(dict(LoadBalancerArn=load_balancer_arn))
    if listener_arns:
        kwargs.update(dict(ListenerArns=listener_arns))
    return client.describe_listeners(**kwargs)
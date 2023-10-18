def describe_target_groups(load_balancer_arn=None, target_group_arns=None, names=None, client=None):
    """
    Permission: elasticloadbalancing:DescribeTargetGroups
    """
    kwargs = dict()
    if load_balancer_arn:
        kwargs.update(LoadBalancerArn=load_balancer_arn)
    if target_group_arns:
        kwargs.update(TargetGroupArns=target_group_arns)
    if names:
        kwargs.update(Names=names)
    return client.describe_target_groups(**kwargs)
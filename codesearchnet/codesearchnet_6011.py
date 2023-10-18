def describe_target_health(target_group_arn, targets=None, client=None):
    """
    Permission: elasticloadbalancing:DescribeTargetHealth
    """
    kwargs = dict(TargetGroupArn=target_group_arn)
    if targets:
        kwargs.update(Targets=targets)
    return client.describe_target_health(**kwargs)['TargetHealthDescriptions']
def describe_rules(listener_arn=None, rule_arns=None, client=None):
    """
    Permission: elasticloadbalancing:DescribeRules
    """
    kwargs = dict()
    if listener_arn:
        kwargs.update(dict(ListenerArn=listener_arn))
    if rule_arns:
        kwargs.update(dict(RuleArns=rule_arns))
    return client.describe_rules(**kwargs)['Rules']
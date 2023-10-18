def get_event(rule, flags=FLAGS.ALL, **conn):
    """
    Orchestrates all the calls required to fully build out a CloudWatch Event Rule in the following format:

    {
        "Arn": ...,
        "Name": ...,
        "Region": ...,
        "Description": ...,
        "State": ...,
        "Rule": ...,
        "Targets" ...,
        "_version": 1
    }

    :param rule: str cloudwatch event name
    :param flags: By default, set to ALL fields
    :param conn: dict containing enough information to make a connection to the desired account.
    Must at least have 'assume_role' key.
    :return: dict containing a fully built out event rule with targets.
    """
    # Python 2 and 3 support:
    try:
        basestring
    except NameError as _:
        basestring = str

    # If string is passed in, determine if it's a name or ARN. Build a dict.
    if isinstance(rule, basestring):
        rule_arn = ARN(rule)
        if rule_arn.error:
            rule_name = rule
        else:
            rule_name = rule_arn.name

    rule = describe_rule(Name=rule_name, **conn)

    return registry.build_out(flags, rule, **conn)
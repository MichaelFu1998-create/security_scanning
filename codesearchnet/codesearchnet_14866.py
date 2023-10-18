def security_group_rule_update(context, rule, **kwargs):
    '''Updates a security group rule.

    NOTE(alexm) this is non-standard functionality.
    '''
    rule.update(kwargs)
    context.session.add(rule)
    return rule
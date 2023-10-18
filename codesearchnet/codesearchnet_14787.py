def update_security_group_rule(context, id, security_group_rule):
    '''Updates a rule and updates the ports'''
    LOG.info("update_security_group_rule for tenant %s" %
             (context.tenant_id))
    new_rule = security_group_rule["security_group_rule"]
    # Only allow updatable fields
    new_rule = _filter_update_security_group_rule(new_rule)

    with context.session.begin():
        rule = db_api.security_group_rule_find(context, id=id,
                                               scope=db_api.ONE)
        if not rule:
            raise sg_ext.SecurityGroupRuleNotFound(id=id)

        db_rule = db_api.security_group_rule_update(context, rule, **new_rule)

        group_id = db_rule.group_id
        group = db_api.security_group_find(context, id=group_id,
                                           scope=db_api.ONE)
        if not group:
            raise sg_ext.SecurityGroupNotFound(id=group_id)

    if group:
        _perform_async_update_rule(context, group_id, group, rule.id,
                                   RULE_UPDATE)

    return v._make_security_group_rule_dict(db_rule)
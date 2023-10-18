def create_security_group_rule(context, security_group_rule):
    """Creates a rule and updates the ports (async) if enabled."""
    LOG.info("create_security_group for tenant %s" %
             (context.tenant_id))
    with context.session.begin():
        rule = _validate_security_group_rule(
            context, security_group_rule["security_group_rule"])
        rule["id"] = uuidutils.generate_uuid()

        group_id = rule["security_group_id"]
        group = db_api.security_group_find(context, id=group_id,
                                           scope=db_api.ONE)
        if not group:
            raise sg_ext.SecurityGroupNotFound(id=group_id)

        quota.QUOTAS.limit_check(
            context, context.tenant_id,
            security_rules_per_group=len(group.get("rules", [])) + 1)

        new_rule = db_api.security_group_rule_create(context, **rule)
    if group:
        _perform_async_update_rule(context, group_id, group, new_rule.id,
                                   RULE_CREATE)
    return v._make_security_group_rule_dict(new_rule)
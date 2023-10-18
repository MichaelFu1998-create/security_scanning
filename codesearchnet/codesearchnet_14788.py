def delete_security_group_rule(context, id):
    """Deletes a rule and updates the ports (async) if enabled."""
    LOG.info("delete_security_group %s for tenant %s" %
             (id, context.tenant_id))
    with context.session.begin():
        rule = db_api.security_group_rule_find(context, id=id,
                                               scope=db_api.ONE)
        if not rule:
            raise sg_ext.SecurityGroupRuleNotFound(id=id)

        group = db_api.security_group_find(context, id=rule["group_id"],
                                           scope=db_api.ONE)
        if not group:
            raise sg_ext.SecurityGroupNotFound(id=id)

        rule["id"] = id
        db_api.security_group_rule_delete(context, rule)
    if group:
        _perform_async_update_rule(context, group.id, group, id, RULE_DELETE)
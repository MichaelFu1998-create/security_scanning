def get_rules(security_group, **kwargs):
    """ format the rule fields to match AWS to support auditor reuse,
        will need to remap back if we want to orchestrate from our stored items """
    rules = security_group.pop('security_group_rules',[])
    for rule in rules:
        rule['ip_protocol'] = rule.pop('protocol')
        rule['from_port'] = rule.pop('port_range_max')
        rule['to_port'] = rule.pop('port_range_min')
        rule['cidr_ip'] = rule.pop('remote_ip_prefix')
        rule['rule_type'] = rule.pop('direction')
    security_group['rules'] = sorted(rules)
    return security_group
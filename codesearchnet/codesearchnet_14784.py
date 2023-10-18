def _filter_update_security_group_rule(rule):
    '''Only two fields are allowed for modification:

        external_service and external_service_id
    '''
    allowed = ['external_service', 'external_service_id']
    filtered = {}
    for k, val in rule.iteritems():
        if k in allowed:
            if isinstance(val, basestring) and \
               len(val) <= GROUP_NAME_MAX_LENGTH:
                filtered[k] = val
    return filtered
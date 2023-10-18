def get_security_group(security_group, flags=FLAGS.ALL, **kwargs):
    result = registry.build_out(flags, start_with=security_group,  pass_datastructure=True, **kwargs)
    """ just store the AWS formatted rules """
    result.pop('security_group_rules', [])
    return result
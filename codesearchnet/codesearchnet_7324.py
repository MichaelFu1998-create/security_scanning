def _dusty_hosts_config(hosts_specs):
    """Return a string of all host rules required to match
    the given spec. This string is wrapped in the Dusty hosts
    header and footer so it can be easily removed later."""
    rules =  ''.join(['{} {}\n'.format(spec['forwarded_ip'], spec['host_address']) for spec in hosts_specs])
    return config_file.create_config_section(rules)
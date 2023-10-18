def update_hosts_file_from_port_spec(port_spec):
    """Given a port spec, update the hosts file specified at
    constants.HOST_PATH to contain the port mappings specified
    in the spec. Any existing Dusty configurations are replaced."""
    logging.info('Updating hosts file to match port spec')
    hosts_specs = port_spec['hosts_file']
    current_hosts = config_file.read(constants.HOSTS_PATH)
    cleared_hosts = config_file.remove_current_dusty_config(current_hosts)
    updated_hosts = cleared_hosts + _dusty_hosts_config(hosts_specs)
    config_file.write(constants.HOSTS_PATH, updated_hosts)
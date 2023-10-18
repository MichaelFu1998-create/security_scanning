def _get_ports_list(app_name, port_specs):
    """ Returns a list of formatted port mappings for an app """
    if app_name not in port_specs['docker_compose']:
        return []
    return ["{}:{}".format(port_spec['mapped_host_port'], port_spec['in_container_port'])
            for port_spec in port_specs['docker_compose'][app_name]]
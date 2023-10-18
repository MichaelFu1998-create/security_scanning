def get_compose_dict(assembled_specs, port_specs):
    """ This function returns a dictionary representation of a docker-compose.yml file, based on assembled_specs from
    the spec_assembler, and port_specs from the port_spec compiler """
    compose_dict = _compose_dict_for_nginx(port_specs)
    for app_name in assembled_specs['apps'].keys():
        compose_dict[app_name] = _composed_app_dict(app_name, assembled_specs, port_specs)
    for service_spec in assembled_specs['services'].values():
        compose_dict[service_spec.name] = _composed_service_dict(service_spec)
    return compose_dict
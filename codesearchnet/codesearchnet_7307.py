def _composed_app_dict(app_name, assembled_specs, port_specs):
    """ This function returns a dictionary of the docker-compose.yml specifications for one app """
    logging.info("Compose Compiler: Compiling dict for app {}".format(app_name))
    app_spec = assembled_specs['apps'][app_name]
    compose_dict = app_spec["compose"]
    _apply_env_overrides(env_overrides_for_app_or_service(app_name), compose_dict)
    if 'image' in app_spec and 'build' in app_spec:
        raise RuntimeError("image and build are both specified in the spec for {}".format(app_name))
    elif 'image' in app_spec:
        logging.info
        compose_dict['image'] = app_spec['image']
    elif 'build' in app_spec:
        compose_dict['build'] = _get_build_path(app_spec)
    else:
        raise RuntimeError("Neither image nor build was specified in the spec for {}".format(app_name))
    compose_dict['entrypoint'] = []
    compose_dict['command'] = _compile_docker_command(app_spec)
    compose_dict['container_name'] = "dusty_{}_1".format(app_name)
    logging.info("Compose Compiler: compiled command {}".format(compose_dict['command']))
    compose_dict['links'] = _links_for_app(app_spec, assembled_specs)
    logging.info("Compose Compiler: links {}".format(compose_dict['links']))
    compose_dict['volumes'] = compose_dict['volumes'] + _get_compose_volumes(app_name, assembled_specs)
    logging.info("Compose Compiler: volumes {}".format(compose_dict['volumes']))
    port_list = _get_ports_list(app_name, port_specs)
    if port_list:
        compose_dict['ports'] = port_list
    logging.info("Compose Compiler: ports {}".format(port_list))
    compose_dict['user'] = 'root'
    return compose_dict
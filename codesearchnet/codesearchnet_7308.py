def _composed_service_dict(service_spec):
    """This function returns a dictionary of the docker_compose specifications
    for one service. Currently, this is just the Dusty service spec with
    an additional volume mount to support Dusty's cp functionality."""
    compose_dict = service_spec.plain_dict()
    _apply_env_overrides(env_overrides_for_app_or_service(service_spec.name), compose_dict)
    compose_dict.setdefault('volumes', []).append(_get_cp_volume_mount(service_spec.name))
    compose_dict['container_name'] = "dusty_{}_1".format(service_spec.name)
    return compose_dict
def _get_compose_volumes(app_name, assembled_specs):
    """ This returns formatted volume specifications for a docker-compose app. We mount the app
    as well as any libs it needs so that local code is used in our container, instead of whatever
    code was in the docker image.

    Additionally, we create a volume for the /cp directory used by Dusty to facilitate
    easy file transfers using `dusty cp`."""
    volumes = []
    volumes.append(_get_cp_volume_mount(app_name))
    volumes += get_app_volume_mounts(app_name, assembled_specs)
    return volumes
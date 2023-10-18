def respawn(name=None, group=None):
    """
    Deletes and recreates one or more VM instances.
    """

    if name is None:
        name = get_name()

    delete(name=name, group=group)
    instance = get_or_create(name=name, group=group)
    env.host_string = instance.public_dns_name
def dependency_sorted(containers):
    """Sort a dictionary or list of containers into dependency order

    Returns a sequence
    """
    if not isinstance(containers, collections.Mapping):
        containers = dict((c.name, c) for c in containers)

    container_links = dict((name, set(c.links.keys()))
                           for name, c in containers.items())
    sorted_names = _resolve(container_links)
    return [containers[name] for name in sorted_names]
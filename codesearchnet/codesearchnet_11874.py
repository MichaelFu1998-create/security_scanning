def record_manifest():
    """
    Called after a deployment to record any data necessary to detect changes
    for a future deployment.
    """
    data = {}
    # Record settings.
    data['settings'] = dict(
        (k, v)
        for k, v in env.items()
        if not isinstance(v, types.GeneratorType) and k.strip() and not k.startswith('_') and not callable(v)
    )
    # Record tarball hash.
    # Record database migrations.
    # Record media hash.
    return data
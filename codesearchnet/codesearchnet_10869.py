def _select_manager(backend_name):
    """Select the proper LockManager based on the current backend used by Celery.

    :raise NotImplementedError: If Celery is using an unsupported backend.

    :param str backend_name: Class name of the current Celery backend. Usually value of
        current_app.extensions['celery'].celery.backend.__class__.__name__.

    :return: Class definition object (not instance). One of the _LockManager* classes.
    """
    if backend_name == 'RedisBackend':
        lock_manager = _LockManagerRedis
    elif backend_name == 'DatabaseBackend':
        lock_manager = _LockManagerDB
    else:
        raise NotImplementedError
    return lock_manager
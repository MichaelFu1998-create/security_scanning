def single_instance(func=None, lock_timeout=None, include_args=False):
    """Celery task decorator. Forces the task to have only one running instance at a time.

    Use with binded tasks (@celery.task(bind=True)).

    Modeled after:
    http://loose-bits.com/2010/10/distributed-task-locking-in-celery.html
    http://blogs.it.ox.ac.uk/inapickle/2012/01/05/python-decorators-with-optional-arguments/

    Written by @Robpol86.

    :raise OtherInstanceError: If another instance is already running.

    :param function func: The function to decorate, must be also decorated by @celery.task.
    :param int lock_timeout: Lock timeout in seconds plus five more seconds, in-case the task crashes and fails to
        release the lock. If not specified, the values of the task's soft/hard limits are used. If all else fails,
        timeout will be 5 minutes.
    :param bool include_args: Include the md5 checksum of the arguments passed to the task in the Redis key. This allows
        the same task to run with different arguments, only stopping a task from running if another instance of it is
        running with the same arguments.
    """
    if func is None:
        return partial(single_instance, lock_timeout=lock_timeout, include_args=include_args)

    @wraps(func)
    def wrapped(celery_self, *args, **kwargs):
        """Wrapped Celery task, for single_instance()."""
        # Select the manager and get timeout.
        timeout = (
            lock_timeout or celery_self.soft_time_limit or celery_self.time_limit
            or celery_self.app.conf.get('CELERYD_TASK_SOFT_TIME_LIMIT')
            or celery_self.app.conf.get('CELERYD_TASK_TIME_LIMIT')
            or (60 * 5)
        )
        manager_class = _select_manager(celery_self.backend.__class__.__name__)
        lock_manager = manager_class(celery_self, timeout, include_args, args, kwargs)

        # Lock and execute.
        with lock_manager:
            ret_value = func(*args, **kwargs)
        return ret_value
    return wrapped
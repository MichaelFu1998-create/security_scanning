def loop_in_background(interval, callback):
    """
    When entering the context, spawns a greenlet that sleeps for `interval` seconds between `callback` executions.
    When leaving the context stops the greenlet.
    The yielded object is the `GeventLoop` object so the loop can be stopped from within the context.

    For example:
    ```
    with loop_in_background(60.0, purge_cache) as purge_cache_job:
        ...
        ...
        if should_stop_cache():
            purge_cache_job.stop()
    ```
    """
    loop = GeventLoop(interval, callback)
    loop.start()
    try:
        yield loop
    finally:
        if loop.has_started():
            loop.stop()
def task(*args, **kwargs):
    """
    Decorator for registering a satchel method as a Fabric task.

    Can be used like:

        @task
        def my_method(self):
            ...

        @task(precursors=['other_satchel'])
        def my_method(self):
            ...

    """
    precursors = kwargs.pop('precursors', None)
    post_callback = kwargs.pop('post_callback', False)
    if args and callable(args[0]):
        # direct decoration, @task
        return _task(*args)

    # callable decoration, @task(precursors=['satchel'])
    def wrapper(meth):
        if precursors:
            meth.deploy_before = list(precursors)
        if post_callback:
            #from burlap.common import post_callbacks
            #post_callbacks.append(meth)
            meth.is_post_callback = True
        return _task(meth)
    return wrapper
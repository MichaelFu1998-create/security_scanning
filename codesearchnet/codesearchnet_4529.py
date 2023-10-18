def bash_app(function=None, data_flow_kernel=None, walltime=60, cache=False, executors='all'):
    """Decorator function for making bash apps.

    Parameters
    ----------
    function : function
        Do not pass this keyword argument directly. This is needed in order to allow for omitted parenthesis,
        for example, `@bash_app` if using all defaults or `@bash_app(walltime=120)`. If the
        decorator is used alone, function will be the actual function being decorated, whereas if it
        is called with arguments, function will be None. Default is None.
    data_flow_kernel : DataFlowKernel
        The :class:`~parsl.dataflow.dflow.DataFlowKernel` responsible for managing this app. This can
        be omitted only after calling :meth:`parsl.dataflow.dflow.DataFlowKernelLoader.load`. Default is None.
    walltime : int
        Walltime for app in seconds. Default is 60.
    executors : string or list
        Labels of the executors that this app can execute over. Default is 'all'.
    cache : bool
        Enable caching of the app call. Default is False.
    """
    from parsl.app.bash import BashApp

    def decorator(func):
        def wrapper(f):
            return BashApp(f,
                           data_flow_kernel=data_flow_kernel,
                           walltime=walltime,
                           cache=cache,
                           executors=executors)
        return wrapper(func)
    if function is not None:
        return decorator(function)
    return decorator
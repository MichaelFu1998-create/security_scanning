def App(apptype, data_flow_kernel=None, walltime=60, cache=False, executors='all'):
    """The App decorator function.

    Args:
        - apptype (string) : Apptype can be bash|python

    Kwargs:
        - data_flow_kernel (DataFlowKernel): The :class:`~parsl.dataflow.dflow.DataFlowKernel` responsible for
          managing this app. This can be omitted only
          after calling :meth:`parsl.dataflow.dflow.DataFlowKernelLoader.load`.
        - walltime (int) : Walltime for app in seconds,
             default=60
        - executors (str|list) : Labels of the executors that this app can execute over. Default is 'all'.
        - cache (Bool) : Enable caching of the app call
             default=False

    Returns:
         A PythonApp or BashApp object, which when called runs the apps through the executor.
    """

    from parsl.app.python import PythonApp
    from parsl.app.bash import BashApp

    logger.warning("The 'App' decorator will be deprecated in Parsl 0.8. Please use 'python_app' or 'bash_app' instead.")

    if apptype == 'python':
        app_class = PythonApp
    elif apptype == 'bash':
        app_class = BashApp
    else:
        raise InvalidAppTypeError("Invalid apptype requested {}; must be 'python' or 'bash'".format(apptype))

    def wrapper(f):
        return app_class(f,
                         data_flow_kernel=data_flow_kernel,
                         walltime=walltime,
                         cache=cache,
                         executors=executors)
    return wrapper
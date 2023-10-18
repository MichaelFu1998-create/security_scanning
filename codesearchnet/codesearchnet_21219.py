def setup_notebook(debug=False):
    """Called at the start of notebook execution to setup the environment.

    This will configure bokeh, and setup the logging library to be
    reasonable."""
    output_notebook(INLINE, hide_banner=True)
    if debug:
        _setup_logging(logging.DEBUG)
        logging.debug('Running notebook in debug mode.')
    else:
        _setup_logging(logging.WARNING)

    # If JUPYTERHUB_SERVICE_PREFIX environment variable isn't set,
    # this means that you're running JupyterHub not with Hub in k8s,
    # and not using run_local.sh (which sets it to empty).
    if 'JUPYTERHUB_SERVICE_PREFIX' not in os.environ:
        global jupyter_proxy_url
        jupyter_proxy_url = 'localhost:8888'
        logging.info('Setting jupyter proxy to local mode.')
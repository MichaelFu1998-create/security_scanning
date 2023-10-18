def teardown(file):  # pylint:disable=redefined-builtin
    """Teardown a polyaxon deployment given a config file."""
    config = read_deployment_config(file)
    manager = DeployManager(config=config, filepath=file)
    exception = None
    try:
        if click.confirm('Would you like to execute pre-delete hooks?', default=True):
            manager.teardown(hooks=True)
        else:
            manager.teardown(hooks=False)
    except Exception as e:
        Printer.print_error('Polyaxon could not teardown the deployment.')
        exception = e

    if exception:
        Printer.print_error('Error message `{}`.'.format(exception))
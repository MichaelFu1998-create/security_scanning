def deploy(file, manager_path, check, dry_run):  # pylint:disable=redefined-builtin
    """Deploy polyaxon."""
    config = read_deployment_config(file)
    manager = DeployManager(config=config,
                            filepath=file,
                            manager_path=manager_path,
                            dry_run=dry_run)
    exception = None
    if check:
        manager.check()
        Printer.print_success('Polyaxon deployment file is valid.')
    else:
        try:
            manager.install()
        except Exception as e:
            Printer.print_error('Polyaxon could not be installed.')
            exception = e

    if exception:
        Printer.print_error('Error message `{}`.'.format(exception))
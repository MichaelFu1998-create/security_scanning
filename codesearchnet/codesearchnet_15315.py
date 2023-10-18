def _iterate_managers(connection, skip):
    """Iterate over instantiated managers."""
    for idx, name, manager_cls in _iterate_manage_classes(skip):
        if name in skip:
            continue

        try:
            manager = manager_cls(connection=connection)
        except TypeError as e:
            click.secho(f'Could not instantiate {name}: {e}', fg='red')
        else:
            yield idx, name, manager
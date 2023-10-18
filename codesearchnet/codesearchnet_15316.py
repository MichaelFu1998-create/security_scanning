def drop(connection, skip):
    """Drop all."""
    for idx, name, manager in _iterate_managers(connection, skip):
        click.secho(f'dropping {name}', fg='cyan', bold=True)
        manager.drop_all()
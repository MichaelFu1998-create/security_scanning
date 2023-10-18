def write(connection, skip, directory, force):
    """Write a BEL namespace names/identifiers to terminology store."""
    os.makedirs(directory, exist_ok=True)
    from .manager.namespace_manager import BELNamespaceManagerMixin
    for idx, name, manager in _iterate_managers(connection, skip):
        if not (isinstance(manager, AbstractManager) and isinstance(manager, BELNamespaceManagerMixin)):
            continue
        click.secho(name, fg='cyan', bold=True)
        if force:
            try:
                click.echo(f'dropping')
                manager.drop_all()
                click.echo('clearing cache')
                clear_cache(name)
                click.echo('populating')
                manager.populate()
            except Exception:
                click.secho(f'{name} failed', fg='red')
                continue

        try:
            r = manager.write_directory(directory)
        except TypeError as e:
            click.secho(f'error with {name}: {e}'.rstrip(), fg='red')
        else:
            if not r:
                click.echo('no update')
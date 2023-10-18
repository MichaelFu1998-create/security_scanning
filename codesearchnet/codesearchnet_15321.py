def actions(connection):
    """List all actions."""
    session = _make_session(connection=connection)
    for action in Action.ls(session=session):
        click.echo(f'{action.created} {action.action} {action.resource}')
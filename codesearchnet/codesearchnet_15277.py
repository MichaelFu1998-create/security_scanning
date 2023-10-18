def add_cli_flask(main: click.Group) -> click.Group:  # noqa: D202
    """Add a ``web`` comand main :mod:`click` function."""

    @main.command()
    @click.option('-v', '--debug', is_flag=True)
    @click.option('-p', '--port')
    @click.option('-h', '--host')
    @click.option('-k', '--secret-key', default=os.urandom(8))
    @click.pass_obj
    def web(manager, debug, port, host, secret_key):
        """Run the web app."""
        if not manager.is_populated():
            click.echo('{} has not yet been populated'.format(manager.module_name))
            sys.exit(0)

        app = manager.get_flask_admin_app(url='/', secret_key=secret_key)
        app.run(debug=debug, host=host, port=port)

    return main
def add_cli_cache(main: click.Group) -> click.Group:  # noqa: D202
    """Add several commands to main :mod:`click` function for handling the cache."""

    @main.group()
    def cache():
        """Manage cached data."""

    @cache.command()
    @click.pass_obj
    def locate(manager):
        """Print the location of the data directory."""
        data_dir = get_data_dir(manager.module_name)
        click.echo(data_dir)

    @cache.command()
    @click.pass_obj
    def ls(manager):
        """List files in the cache."""
        data_dir = get_data_dir(manager.module_name)

        for path in os.listdir(data_dir):
            click.echo(path)

    @cache.command()
    @click.pass_obj
    def clear(manager):
        """Clear all files from the cache."""
        clear_cache(manager.module_name)

    return main
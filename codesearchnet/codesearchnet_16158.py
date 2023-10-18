def cli(ctx, version):
    """Bottery"""

    # If no subcommand was given and the version flag is true, shows
    # Bottery version
    if not ctx.invoked_subcommand and version:
        click.echo(bottery.__version__)
        ctx.exit()

    # If no subcommand but neither the version flag, shows help message
    elif not ctx.invoked_subcommand:
        click.echo(ctx.get_help())
        ctx.exit()
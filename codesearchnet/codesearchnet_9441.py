def config(ctx, key, value, remove, edit):
    """Get or set config item."""
    conf = ctx.obj["conf"]

    if not edit and not key:
        raise click.BadArgumentUsage("You have to specify either a key or use --edit.")

    if edit:
        return click.edit(filename=conf.config_file)

    if remove:
        try:
            conf.cfg.remove_option(key[0], key[1])
        except Exception as e:
            logger.debug(e)
        else:
            conf.write_config()
        return

    if not value:
        try:
            click.echo(conf.cfg.get(key[0], key[1]))
        except Exception as e:
            logger.debug(e)
        return

    if not conf.cfg.has_section(key[0]):
        conf.cfg.add_section(key[0])

    conf.cfg.set(key[0], key[1], value)
    conf.write_config()
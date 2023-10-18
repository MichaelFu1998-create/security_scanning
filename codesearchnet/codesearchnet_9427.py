def validate_config_key(ctx, param, value):
    """Validate a configuration key according to `section.item`."""
    if not value:
        return value

    try:
        section, item = value.split(".", 1)
    except ValueError:
        raise click.BadArgumentUsage("Given key does not contain a section name.")
    else:
        return section, item
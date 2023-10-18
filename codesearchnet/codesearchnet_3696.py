def secho(message, **kwargs):
    """A wrapper around click.secho that disables any coloring being used
    if colors have been disabled.
    """
    # If colors are disabled, remove any color or other style data
    # from keyword arguments.
    if not settings.color:
        for key in ('fg', 'bg', 'bold', 'blink'):
            kwargs.pop(key, None)

    # Okay, now call click.secho normally.
    return click.secho(message, **kwargs)
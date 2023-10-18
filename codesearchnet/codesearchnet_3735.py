def _echo_setting(key):
    """Echo a setting to the CLI."""
    value = getattr(settings, key)
    secho('%s: ' % key, fg='magenta', bold=True, nl=False)
    secho(
        six.text_type(value),
        bold=True,
        fg='white' if isinstance(value, six.text_type) else 'cyan',
    )
def get_configuration_value(val_name, default=None, **kwargs):
    """
    Get a configuration value, or fall back to ``default`` if it doesn't exist.

    Also takes a `type` argument to guide which particular upstream method to use when trying to retrieve a value.
    Current types include:
        - `url` to specifically get a URL.
    """
    if kwargs.get('type') == 'url':
        return get_url(val_name) or default if callable(get_url) else default
    return configuration_helpers.get_value(val_name, default, **kwargs) if configuration_helpers else default
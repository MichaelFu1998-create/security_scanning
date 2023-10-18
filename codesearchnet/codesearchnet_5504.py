def get_app_kwarg_dict(appInstance=None):
    """Returns the dictionary of CORS specific app configurations."""
    app = (appInstance or current_app)

    # In order to support blueprints which do not have a config attribute
    app_config = getattr(app, 'config', {})

    return {
        k.lower().replace('cors_', ''): app_config.get(k)
        for k in CONFIG_OPTIONS
        if app_config.get(k) is not None
    }
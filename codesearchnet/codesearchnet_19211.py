def config_loader(app, **kwargs_config):
    """Configuration loader.

    Adds support for loading templates from the Flask application's instance
    folder (``<instance_folder>/templates``).
    """
    # This is the only place customize the Flask application right after
    # it has been created, but before all extensions etc are loaded.
    local_templates_path = os.path.join(app.instance_path, 'templates')
    if os.path.exists(local_templates_path):
        # Let's customize the template loader to look into packages
        # and application templates folders.
        app.jinja_loader = ChoiceLoader([
            FileSystemLoader(local_templates_path),
            app.jinja_loader,
        ])

    app.jinja_options = dict(
        app.jinja_options,
        cache_size=1000,
        bytecode_cache=BytecodeCache(app)
    )

    invenio_config_loader(app, **kwargs_config)
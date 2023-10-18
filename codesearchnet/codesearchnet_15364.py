def includeme(config):
    """Declare all routes."""
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')
    config.add_jinja2_renderer('.rss')
    config.add_static_view(name='/a/static', path="cnxpublishing:static/")

    # Commit the configuration otherwise the jija2_env won't have
    # a `globals` assignment.
    config.commit()

    # Place a few globals in the template environment.
    from cnxdb.ident_hash import join_ident_hash
    for ext in ('.html', '.rss',):
        jinja2_env = config.get_jinja2_environment(ext)
        jinja2_env.globals.update(
            join_ident_hash=join_ident_hash,
        )

    declare_api_routes(config)
    declare_browsable_routes(config)
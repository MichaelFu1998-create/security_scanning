def config_sources(app, environment, cluster, configs_dirs, app_dir,
                   local=False, build=False):
    """Return the config files for an environment & cluster specific app."""
    sources = [
        # Machine-specific
        (configs_dirs, 'hostname'),
        (configs_dirs, 'hostname-local'),
        (configs_dirs, 'hostname-build'),
        # Global
        (configs_dirs, 'common'),
        # Environment + Cluster
        (configs_dirs, 'common-%s' % environment),
        (configs_dirs, 'common-%s-%s' % (environment, cluster)),
        (configs_dirs, 'common-local'),
        (configs_dirs, 'common-build'),
        # Machine-specific overrides
        (configs_dirs, 'common-overrides'),
        # Application-specific
        ([app_dir], '%s-default' % app),
        ([app_dir], '%s-%s' % (app, environment)),
        ([app_dir], '%s-%s-%s' % (app, environment, cluster)),
        (configs_dirs, app),
        (configs_dirs, '%s-%s' % (app, environment)),
        (configs_dirs, '%s-%s-%s' % (app, environment, cluster)),
        ([app_dir], '%s-local' % app),
        ([app_dir], '%s-build' % app),
        (configs_dirs, '%s-local' % app),
        (configs_dirs, '%s-build' % app),
        # Machine-specific application override
        (configs_dirs, '%s-overrides' % app),
    ]

    # Filter out build sources if not requested
    if not build:
        sources = [source for source in sources
                   if not source[1].endswith('-build')]
        # Filter out local sources if not build and not local
        if not local:
            sources = [source for source in sources
                       if not source[1].endswith('-local')]

    return available_sources(sources)
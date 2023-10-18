def _make_celery_app(config):
    """This exposes the celery app. The app is actually created as part
    of the configuration. However, this does make the celery app functional
    as a stand-alone celery application.

    This puts the pyramid configuration object on the celery app to be
    used for making the registry available to tasks running inside the
    celery worker process pool. See ``CustomTask.__call__``.

    """
    # Tack the pyramid config on the celery app for later use.
    config.registry.celery_app.conf['pyramid_config'] = config
    return config.registry.celery_app
def initialize_sentry_integration():  # pragma: no cover
    """\
    Used to optionally initialize the Sentry service with this app.
    See https://docs.sentry.io/platforms/python/pyramid/

    """
    # This function is not under coverage because it is boilerplate
    # from the Sentry documentation.
    try:
        import sentry_sdk
        from sentry_sdk.integrations.pyramid import PyramidIntegration
        from sentry_sdk.integrations.celery import CeleryIntegration
    except ImportError:
        warnings.warn(
            "Sentry is not configured because the Sentry SDK "
            "(sentry_sdk package) is not installed",
            UserWarning,
        )
        return  # bail out early

    try:
        dsn = os.environ['SENTRY_DSN']
    except KeyError:
        warnings.warn(
            "Sentry is not configured because SENTRY_DSN "
            "was not supplied.",
            UserWarning,
        )
    else:
        sentry_sdk.init(
            dsn=dsn,
            integrations=[PyramidIntegration(), CeleryIntegration()],
        )
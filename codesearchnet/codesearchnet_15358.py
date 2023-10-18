def task(**kwargs):
    """A function task decorator used in place of ``@celery_app.task``."""

    def wrapper(wrapped):

        def callback(scanner, name, obj):
            celery_app = scanner.config.registry.celery_app
            celery_app.task(**kwargs)(obj)

        venusian.attach(wrapped, callback)
        return wrapped

    return wrapper
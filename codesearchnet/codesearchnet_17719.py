def models_preparing(app):
    """ Wrap all sqlalchemy model in settings.
    """

    def wrapper(resource, parent):
        if isinstance(resource, DeclarativeMeta):
            resource = ListResource(resource)
        if not getattr(resource, '__parent__', None):
            resource.__parent__ = parent
        return resource

    resources_preparing_factory(app, wrapper)
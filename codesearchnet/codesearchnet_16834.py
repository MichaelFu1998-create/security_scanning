def index(method=None, delete=False):
    """Decorator to update index.

    :param method: Function wrapped. (Default: ``None``)
    :param delete: If `True` delete the indexed record. (Default: ``None``)
    """
    if method is None:
        return partial(index, delete=delete)

    @wraps(method)
    def wrapper(self_or_cls, *args, **kwargs):
        """Send record for indexing."""
        result = method(self_or_cls, *args, **kwargs)
        try:
            if delete:
                self_or_cls.indexer.delete(result)
            else:
                self_or_cls.indexer.index(result)
        except RequestError:
            current_app.logger.exception('Could not index {0}.'.format(result))
        return result
    return wrapper
def log_update(entity, update):
    """Logs an update done on an entity
    """
    p = {'on': entity, 'update': update}
    _log(TYPE_CODES.UPDATE, p)
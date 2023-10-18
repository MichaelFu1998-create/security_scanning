def log_entity_deletion(entity, params=None):
    """Logs an entity creation
    """
    p = {'entity': entity}
    if params:
        p['params'] = params
    _log(TYPE_CODES.DELETE, p)
def log_entity_creation(entity, params=None):
    """Logs an entity creation
    """
    p = {'entity': entity}
    if params:
        p['params'] = params
    _log(TYPE_CODES.CREATE, p)
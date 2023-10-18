def log_operation(entities, operation_name, params=None):
    """Logs an operation done on an entity, possibly with other arguments
    """
    if isinstance(entities, (list, tuple)):
        entities = list(entities)
    else:
        entities = [entities]

    p = {'name': operation_name, 'on': entities}
    if params:
        p['params'] = params
    _log(TYPE_CODES.OPERATION, p)
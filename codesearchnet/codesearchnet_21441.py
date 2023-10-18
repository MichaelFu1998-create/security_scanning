def log_state(entity, state):
    """Logs a new state of an entity
    """
    p = {'on': entity, 'state': state}
    _log(TYPE_CODES.STATE, p)
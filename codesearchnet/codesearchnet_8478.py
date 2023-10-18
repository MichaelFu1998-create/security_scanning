def soft_fail(msg=''):
    """Adds error message to soft errors list if within soft assertions context.
       Either just force test failure with the given message."""
    global _soft_ctx
    if _soft_ctx:
        global _soft_err
        _soft_err.append('Fail: %s!' % msg if msg else 'Fail!')
        return
    fail(msg)
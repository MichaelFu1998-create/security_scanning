def require_template_debug(f):
    """Decorated function is a no-op if TEMPLATE_DEBUG is False"""
    def _(*args, **kwargs):
        TEMPLATE_DEBUG = getattr(settings, 'TEMPLATE_DEBUG', False)
        return f(*args, **kwargs) if TEMPLATE_DEBUG else ''
    return _
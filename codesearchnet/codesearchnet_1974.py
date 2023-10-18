def register_dialect(name, dialect=None, **kwargs):
    """Create a mapping from a string name to a dialect class.
    dialect = csv.register_dialect(name, dialect)"""
    if not isinstance(name, basestring):
        raise TypeError("dialect name must be a string or unicode")

    dialect = _call_dialect(dialect, kwargs)
    _dialects[name] = dialect
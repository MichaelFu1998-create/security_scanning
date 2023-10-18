def get(name=None):
    """
    Return a named Palette, or None if no such name exists.

    If ``name`` is omitted, the default value is used.
    """
    if name is None or name == 'default':
        return _DEFAULT_PALETTE

    if isinstance(name, str):
        return PROJECT_PALETTES.get(name) or BUILT_IN_PALETTES.get(name)
def get_group(name: str) -> _Group:
    """
    Get a configuration variable group named |name|
    """
    global _groups

    if name in _groups:
        return _groups[name]

    group = _Group(name)
    _groups[name] = group

    return group
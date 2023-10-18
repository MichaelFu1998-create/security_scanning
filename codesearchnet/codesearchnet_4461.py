def uncan(obj, g=None):
    """Invert canning."""
    import_needed = False
    for cls, uncanner in iteritems(uncan_map):
        if isinstance(cls, string_types):
            import_needed = True
            break
        elif isinstance(obj, cls):
            return uncanner(obj, g)

    if import_needed:
        # perform uncan_map imports, then try again
        # this will usually only happen once
        _import_mapping(uncan_map, _original_uncan_map)
        return uncan(obj, g)

    return obj
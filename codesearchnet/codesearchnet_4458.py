def can(obj):
    """Prepare an object for pickling."""
    import_needed = False

    for cls, canner in iteritems(can_map):
        if isinstance(cls, string_types):
            import_needed = True
            break
        elif istype(obj, cls):
            return canner(obj)

    if import_needed:
        # perform can_map imports, then try again
        # this will usually only happen once
        _import_mapping(can_map, _original_can_map)
        return can(obj)

    return obj
def patch_locals(depth=2):
    """Temporarily (see unpatch_locals()) replaces all module variables
    considered preferences with PatchedLocal objects, so that every
    variable has different hash returned by id().

    """
    for name, locals_dict in traverse_local_prefs(depth):
        locals_dict[name] = PatchedLocal(name, locals_dict[name])

    get_frame_locals(depth)[__PATCHED_LOCALS_SENTINEL] = True
def unpatch_locals(depth=3):
    """Restores the original values of module variables
    considered preferences if they are still PatchedLocal
    and not PrefProxy.

    """
    for name, locals_dict in traverse_local_prefs(depth):
        if isinstance(locals_dict[name], PatchedLocal):
            locals_dict[name] = locals_dict[name].val

    del get_frame_locals(depth)[__PATCHED_LOCALS_SENTINEL]
def traverse_local_prefs(stepback=0):
    """Generator to walk through variables considered as preferences
    in locals dict of a given frame.

    :param int stepback:

    :rtype: tuple

    """
    locals_dict = get_frame_locals(stepback+1)
    for k in locals_dict:
        if not k.startswith('_') and k.upper() == k:
            yield k, locals_dict
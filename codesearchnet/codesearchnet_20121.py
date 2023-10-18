def get_frame_locals(stepback=0):
    """Returns locals dictionary from a given frame.

    :param int stepback:

    :rtype: dict

    """
    with Frame(stepback=stepback) as frame:
        locals_dict = frame.f_locals

    return locals_dict
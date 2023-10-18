def grab(bbox=None, childprocess=None, backend=None):
    """Copy the contents of the screen to PIL image memory.

    :param bbox: optional bounding box (x1,y1,x2,y2)
    :param childprocess: pyscreenshot can cause an error,
            if it is used on more different virtual displays
            and back-end is not in different process.
            Some back-ends are always different processes: scrot, imagemagick
            The default is False if the program was started inside IDLE,
            otherwise it is True.
    :param backend: back-end can be forced if set (examples:scrot, wx,..),
                    otherwise back-end is automatic
    """
    if childprocess is None:
        childprocess = childprocess_default_value()
    return _grab(
        to_file=False, childprocess=childprocess, backend=backend, bbox=bbox)
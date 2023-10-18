def grab_to_file(filename, childprocess=None, backend=None):
    """Copy the contents of the screen to a file. Internal function! Use
    PIL.Image.save() for saving image to file.

    :param filename: file for saving
    :param childprocess: see :py:func:`grab`
    :param backend: see :py:func:`grab`
    """
    if childprocess is None:
        childprocess = childprocess_default_value()
    return _grab(to_file=True, childprocess=childprocess,
                 backend=backend, filename=filename)
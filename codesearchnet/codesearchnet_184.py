def warn_deprecated(msg, stacklevel=2):
    """Generate a non-silent deprecation warning with stacktrace.

    The used warning is ``imgaug.imgaug.DeprecationWarning``.

    Parameters
    ----------
    msg : str
        The message of the warning.

    stacklevel : int, optional
        How many steps above this function to "jump" in the stacktrace for
        the displayed file and line number of the error message.
        Usually 2.

    """
    import warnings
    warnings.warn(msg,
                  category=DeprecationWarning,
                  stacklevel=stacklevel)
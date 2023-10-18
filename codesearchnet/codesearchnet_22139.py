def fopen(name, mode='r', buffering=-1):
    """Similar to Python's built-in `open()` function."""
    f = _fopen(name, mode, buffering)
    return _FileObjectThreadWithContext(f, mode, buffering)
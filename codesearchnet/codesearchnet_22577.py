def open(name=None, fileobj=None, closefd=True):
    """
    Use all decompressor possible to make the stream
    """
    return Guesser().open(name=name, fileobj=fileobj, closefd=closefd)
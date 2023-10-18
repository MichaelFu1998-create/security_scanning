def withextsep(extensions):
    """Return list in which each element is guaranteed to start with :data:`os.path.extsep`."""
    def dottify(x):
        if x.startswith(os.path.extsep):
            return x
        return os.path.extsep + x
    return [dottify(x) for x in asiterable(extensions)]
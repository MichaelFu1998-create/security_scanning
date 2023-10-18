def all_subclasses(cls):
    """ Recursively generate of all the subclasses of class cls. """
    for subclass in cls.__subclasses__():
        yield subclass
        for subc in all_subclasses(subclass):
            yield subc
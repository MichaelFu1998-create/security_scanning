def xformer(signature):
    """
    Returns a transformer function for the given signature.

    :param str signature: a dbus signature
    :returns: a function to transform a list of objects to inhabit the signature
    :rtype: (list of object) -> (list of object)
    """

    funcs = [f for (f, _) in xformers(signature)]

    def the_func(objects):
        """
        Returns the a list of objects, transformed.

        :param objects: a list of objects
        :type objects: list of object

        :returns: transformed objects
        :rtype: list of object (in dbus types)
        """
        if len(objects) != len(funcs):
            raise IntoDPValueError(
                objects,
                "objects",
                "must have exactly %u items, has %u" % \
                  (len(funcs), len(objects))
            )
        return [x for (x, _) in (f(a) for (f, a) in zip(funcs, objects))]

    return the_func
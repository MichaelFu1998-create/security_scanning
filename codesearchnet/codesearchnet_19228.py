def flag_inner_classes(obj):
    """
    Mutates any attributes on ``obj`` which are classes, with link to ``obj``.

    Adds a convenience accessor which instantiates ``obj`` and then calls its
    ``setup`` method.

    Recurses on those objects as well.
    """
    for tup in class_members(obj):
        tup[1]._parent = obj
        tup[1]._parent_inst = None
        tup[1].__getattr__ = my_getattr
        flag_inner_classes(tup[1])
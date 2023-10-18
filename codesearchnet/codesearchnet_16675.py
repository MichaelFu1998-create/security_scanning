def defcells(space=None, name=None, *funcs):
    """Decorator/function to create cells from Python functions.

    Convenience decorator/function to create new cells directly from function
    definitions or function objects substituting for calling
    :py:meth:`new_cells <modelx.core.space.StaticSpace.new_cells>`
    method of the parent space.

    There are 3 ways to use ``defcells`` to define cells from functions.

    **1. As a decorator without arguments**

    To create a cells from a function definition in the current space of the
    current model with the same name as the function's::

        @defcells
        def foo(x):
            return x

    **2. As a decorator with arguments**

    To create a cells from a function definition in a given space and/or with
    a given name::

        @defcells(space=space, name=name)
        def foo(x):
            return x

    **3. As a function**

    To create a multiple cells from a multiple function definitions::

        def foo(x):
            return x

        def bar(y):
            return foo(y)

        foo, bar = defcells(foo, bar)

    Args:
        space(optional): For the 2nd usage, a space to create the cells in.
            Defaults to the current space of the current model.
        name(optional): For the 2nd usage, a name of the created cells.
            Defaults to the function name.
        *funcs: For the 3rd usage, function objects. (``space`` and ``name``
            also take function objects for the 3rd usage.)

    Returns:
        For the 1st and 2nd usage, the newly created single cells is returned.
        For the 3rd usage, a list of newly created cells are returned.

    """
    if isinstance(space, _FunctionType) and name is None:
        # called as a function decorator
        func = space
        return _system.currentspace.new_cells(formula=func).interface

    elif (isinstance(space, _Space) or space is None) and (
        isinstance(name, str) or name is None
    ):
        # return decorator itself
        if space is None:
            space = _system.currentspace.interface

        return _CellsMaker(space=space._impl, name=name)

    elif all(
        isinstance(func, _FunctionType) for func in (space, name) + funcs
    ):

        return [defcells(func) for func in (space, name) + funcs]

    else:
        raise TypeError("invalid defcells arguments")
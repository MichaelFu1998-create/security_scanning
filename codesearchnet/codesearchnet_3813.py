def command(method=None, **kwargs):
    """Mark this method as a CLI command.

    This will only have any meaningful effect in methods that are members of a
    Resource subclass.
    """
    # Create the actual decorator to be applied.
    # This is done in such a way to make `@resources.command`,
    # `@resources.command()`, and `@resources.command(foo='bar')` all work.
    def actual_decorator(method):
        method._cli_command = True
        method._cli_command_attrs = kwargs
        return method

    # If we got the method straight-up, apply the decorator and return
    # the decorated method; otherwise, return the actual decorator for
    # the Python interpreter to apply.
    if method and isinstance(method, types.FunctionType):
        return actual_decorator(method)
    else:
        return actual_decorator
def is_valid_in_template(var, attr):
    """
    Given a variable and one of its attributes, determine if the attribute is
    accessible inside of a Django template and return True or False accordingly
    """
    # Remove private variables or methods
    if attr.startswith('_'):
        return False
    # Remove any attributes that raise an acception when read
    try:
        value = getattr(var, attr)
    except:
        return False
    if isroutine(value):
        # Remove any routines that are flagged with 'alters_data'
        if getattr(value, 'alters_data', False):
            return False
        else:
            # Remove any routines that require arguments
            try:
                argspec = getargspec(value)
                num_args = len(argspec.args) if argspec.args else 0
                num_defaults = len(argspec.defaults) if argspec.defaults else 0
                if num_args - num_defaults > 1:
                    return False
            except TypeError:
                # C extension callables are routines, but getargspec fails with
                # a TypeError when these are passed.
                pass
    return True
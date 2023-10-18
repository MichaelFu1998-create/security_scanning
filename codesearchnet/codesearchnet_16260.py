def get_attributes(var):
    """
    Given a varaible, return the list of attributes that are available inside
    of a template
    """
    is_valid = partial(is_valid_in_template, var)
    return list(filter(is_valid, dir(var)))
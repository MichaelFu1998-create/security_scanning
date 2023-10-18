def modify(item, output='camelized'):
    """
    Calls _modify and either passes the inflection.camelize method or the inflection.underscore method.

    :param item: dictionary representing item to be modified
    :param output: string 'camelized' or 'underscored'
    :return:
    """
    if output == 'camelized':
        return _modify(item, camelize)
    elif output == 'underscored':
        return _modify(item, underscore)
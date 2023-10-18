def get_item_creator(item_type):
    """Get item creator according registered item type.

    :param item_type: The type of item to be checed.
    :type item_type: types.TypeType.
    :returns: Creator function. None if type not found.
    """
    if item_type not in Pipe.pipe_item_types:
        for registered_type in Pipe.pipe_item_types:
            if issubclass(item_type, registered_type):
                return Pipe.pipe_item_types[registered_type]
        return None
    else:
        return Pipe.pipe_item_types[item_type]
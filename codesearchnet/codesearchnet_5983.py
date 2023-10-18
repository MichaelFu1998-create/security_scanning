def get_item(item, **kwargs):
    """
    API versioning for each OpenStack service is independent. Generically capture
        the public members (non-routine and non-private) of the OpenStack SDK objects.

    Note the lack of the modify_output decorator. Preserving the field naming allows
        us to reconstruct objects and orchestrate from stored items.
    """
    _item = {}
    for k,v in inspect.getmembers(item, lambda a:not(inspect.isroutine(a))):
        if not k.startswith('_') and not k in ignore_list:
            _item[k] = v

    return sub_dict(_item)
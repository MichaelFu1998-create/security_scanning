def update_field_from_proxy(field_obj, pref_proxy):
    """Updates field object with data from a PrefProxy object.

    :param models.Field field_obj:

    :param PrefProxy pref_proxy:

    """
    attr_names = ('verbose_name', 'help_text', 'default')

    for attr_name in attr_names:
        setattr(field_obj, attr_name, getattr(pref_proxy, attr_name))
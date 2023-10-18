def get_field_for_proxy(pref_proxy):
    """Returns a field object instance for a given PrefProxy object.

    :param PrefProxy pref_proxy:

    :rtype: models.Field

    """
    field = {
        bool: models.BooleanField,
        int:  models.IntegerField,
        float: models.FloatField,
        datetime: models.DateTimeField,

    }.get(type(pref_proxy.default), models.TextField)()

    update_field_from_proxy(field, pref_proxy)

    return field
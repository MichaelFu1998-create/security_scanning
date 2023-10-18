def _plugin_endpoint_rename(fn_name, instance):
    """ Rename endpoint function name to avoid conflict when namespacing is set to true

    :param fn_name: Name of the route function
    :param instance: Instance bound to the function
    :return: Name of the new namespaced function name
    """

    if instance and instance.namespaced:
        fn_name = "r_{0}_{1}".format(instance.name, fn_name[2:])
    return fn_name
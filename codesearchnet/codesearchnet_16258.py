def get_details(var):
    """
    Given a variable inside the context, obtain the attributes/callables,
    their values where possible, and the module name and class name if possible
    """
    var_data = {}
    # Obtain module and class details if available and add them in
    module = getattr(var, '__module__', '')
    kls = getattr(getattr(var, '__class__', ''), '__name__', '')
    if module:
        var_data['META_module_name'] = module
    if kls:
        var_data['META_class_name'] = kls
    for attr in get_attributes(var):
        value = _get_detail_value(var, attr)
        if value is not None:
            var_data[attr] = value
    return var_data
def merge_config(template, config, list_identifiers=None):
    """
    Merges ``config`` on top of ``template``.

    Conflicting keys are handled in the following way:

    * simple values (eg: ``str``, ``int``, ``float``, ecc) in ``config`` will
      overwrite the ones in ``template``
    * values of type ``list`` in both ``config`` and ``template`` will be
      merged using to the ``merge_list`` function
    * values of type ``dict`` will be merged recursively

    :param template: template ``dict``
    :param config: config ``dict``
    :param list_identifiers: ``list`` or ``None``
    :returns: merged ``dict``
    """
    result = template.copy()
    for key, value in config.items():
        if isinstance(value, dict):
            node = result.get(key, OrderedDict())
            result[key] = merge_config(node, value)
        elif isinstance(value, list) and isinstance(result.get(key), list):
            result[key] = merge_list(result[key], value, list_identifiers)
        else:
            result[key] = value
    return result
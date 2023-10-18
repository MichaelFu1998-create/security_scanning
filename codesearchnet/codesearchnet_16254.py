def _display_details(var_data):
    """
    Given a dictionary of variable attribute data from get_details display the
    data in the terminal.
    """
    meta_keys = (key for key in list(var_data.keys())
                 if key.startswith('META_'))
    for key in meta_keys:
        display_key = key[5:].capitalize()
        pprint('{0}: {1}'.format(display_key, var_data.pop(key)))
    pprint(var_data)
def get_new_call(group_name, app_name, search_path, filename, require_load,
                 version, secure):
    # type: (str, str, Optional[str], str, bool, Optional[str], bool) -> str
    '''
    Build a call to use the new ``get_config`` function from args passed to
    ``Config.__init__``.
    '''
    new_call_kwargs = {
        'group_name': group_name,
        'filename': filename
    }  # type: Dict[str, Any]
    new_call_lookup_options = {}  # type: Dict[str, Any]
    new_call_lookup_options['secure'] = secure
    if search_path:
        new_call_lookup_options['search_path'] = search_path
    if require_load:
        new_call_lookup_options['require_load'] = require_load
    if version:
        new_call_lookup_options['version'] = version
    if new_call_lookup_options:
        new_call_kwargs['lookup_options'] = new_call_lookup_options

    output = build_call_str('get_config', (app_name,), new_call_kwargs)
    return output
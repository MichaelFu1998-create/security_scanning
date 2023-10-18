def _expand_libs_in_libs(specs):
    """
    Expands specs.libs.depends.libs to include any indirectly required libs
    """
    for lib_name, lib_spec in specs['libs'].iteritems():
        if 'depends' in lib_spec and 'libs' in lib_spec['depends']:
            lib_spec['depends']['libs'] = _get_dependent('libs', lib_name, specs, 'libs')
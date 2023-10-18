def identify_names(code):
    """Builds a codeobj summary by identifying and resolving used names

    >>> code = '''
    ... from a.b import c
    ... import d as e
    ... print(c)
    ... e.HelloWorld().f.g
    ... '''
    >>> for name, o in sorted(identify_names(code).items()):
    ...     print(name, o['name'], o['module'], o['module_short'])
    c c a.b a.b
    e.HelloWorld HelloWorld d d
    """
    finder = NameFinder()
    finder.visit(ast.parse(code))

    example_code_obj = {}
    for name, full_name in finder.get_mapping():
        # name is as written in file (e.g. np.asarray)
        # full_name includes resolved import path (e.g. numpy.asarray)
        module, attribute = full_name.rsplit('.', 1)
        # get shortened module name
        module_short = get_short_module_name(module, attribute)
        cobj = {'name': attribute, 'module': module,
                'module_short': module_short}
        example_code_obj[name] = cobj
    return example_code_obj
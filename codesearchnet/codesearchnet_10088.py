def _get_func_info(docstring, def_lineno, code_lines, prefix):
    """
    Extracts the function signature and description of a Python function

    :param docstring:
        A unicode string of the docstring for the function

    :param def_lineno:
        An integer line number that function was defined on

    :param code_lines:
        A list of unicode string lines from the source file the function was
        defined in

    :param prefix:
        A prefix to prepend to all output lines

    :return:
        A 2-element tuple:

         - [0] A unicode string of the function signature with a docstring of
               parameter info
         - [1] A markdown snippet of the function description
    """

    def_index = def_lineno - 1
    definition = code_lines[def_index]
    definition = definition.rstrip()
    while not definition.endswith(':'):
        def_index += 1
        definition += '\n' + code_lines[def_index].rstrip()

    definition = textwrap.dedent(definition).rstrip(':')
    definition = definition.replace('\n', '\n' + prefix)

    description = ''
    found_colon = False

    params = ''

    for line in docstring.splitlines():
        if line and line[0] == ':':
            found_colon = True
        if not found_colon:
            if description:
                description += '\n'
            description += line
        else:
            if params:
                params += '\n'
            params += line

    description = description.strip()
    description_md = ''
    if description:
        description_md = "%s%s" % (prefix, description.replace('\n', '\n' + prefix))
        description_md = re.sub('\n>(\\s+)\n', '\n>\n', description_md)

    params = params.strip()
    if params:
        definition += (':\n%s    """\n%s    ' % (prefix, prefix))
        definition += params.replace('\n', '\n%s    ' % prefix)
        definition += ('\n%s    """' % prefix)
        definition = re.sub('\n>(\\s+)\n', '\n>\n', definition)

    for search, replace in definition_replacements.items():
        definition = definition.replace(search, replace)

    return (definition, description_md)
def _parse_file(filename, relpath=None):
    """
    Return a list of :class:`_PyconfigCall` from parsing `filename`.

    :param filename: A file to parse
    :param relpath: Relative directory to strip (optional)
    :type filename: str
    :type relpath: str

    """
    with open(filename, 'r') as source:
        source = source.read()

    pyconfig_calls = []
    try:
        nodes = ast.parse(source, filename=filename)
    except SyntaxError:
        # XXX(Jake): We might want to handle this differently
        return []

    # Look for UTF-8 encoding
    first_lines = source[0:200]
    match = re.match('^#.*coding[:=].?([a-zA-Z0-9-_]+).*', first_lines)
    if match:
        try:
            coding = match.group(1)
            source = source.decode(coding)
        except:
            print("# Error decoding file, may not parse correctly:", filename)

    try:
        # Split the source into lines so we can reference it easily
        source = source.split('\n')
    except:
        print("# Error parsing file, ignoring:", filename);
        return []

    # Make the filename relative to the given path, if needed
    if relpath:
        filename = os.path.relpath(filename, relpath)

    for call in ast.walk(nodes):
        if not isinstance(call, _ast.Call):
            # Skip any node that isn't a Call
            continue

        func = call.func
        if not isinstance(call.func, _ast.Attribute):
            # We're looking for calls to pyconfig.*, so the function has to be
            # an Attribute node, otherwise skip it
            continue

        if getattr(func.value, 'id', None) != 'pyconfig':
            # If the Attribute value isn't a Name (doesn't have an `id`) or it
            # isn't 'pyconfig', then we skip
            continue

        if func.attr not in ['get', 'set', 'setting']:
            # If the Attribute attr isn't one of the pyconfig API methods, then
            # we skip
            continue

        # Now we parse the call arguments as best we can
        args = []
        if call.args:
            arg = call.args[0]
            if isinstance(arg, _ast.Str):
                args.append(arg.s)
            else:
                args.append(_map_arg(arg))

        for arg in call.args[1:]:
            args.append(_map_arg(arg))

        line = (filename, source[call.lineno-1], call.lineno, call.col_offset)
        call = _PyconfigCall(func.attr, args[0], args[1:], line)
        pyconfig_calls.append(call)

    return pyconfig_calls
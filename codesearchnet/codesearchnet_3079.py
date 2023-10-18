def translate_js_with_compilation_plan(js, HEADER=DEFAULT_HEADER):
    """js has to be a javascript source code.
       returns equivalent python code.

       compile plans only work with the following restrictions:
       - only enabled for oneliner expressions
       - when there are comments in the js code string substitution is disabled
       - when there nested escaped quotes string substitution is disabled, so

       cacheable:
       Q1 == 1 && name == 'harry'

       not cacheable:
       Q1 == 1 && name == 'harry' // some comment

       not cacheable:
       Q1 == 1 && name == 'o\'Reilly'

       not cacheable:
       Q1 == 1 && name /* some comment */ == 'o\'Reilly'
       """

    match_increaser_str, match_increaser_num, compilation_plan = get_compilation_plan(
        js)

    cp_hash = hashlib.md5(compilation_plan.encode('utf-8')).digest()
    try:
        python_code = cache[cp_hash]['proto_python_code']
    except:
        parser = pyjsparser.PyJsParser()
        parsed = parser.parse(compilation_plan)  # js to esprima syntax tree
        # Another way of doing that would be with my auto esprima translation but its much slower and causes import problems:
        # parsed = esprima.parse(js).to_dict()
        translating_nodes.clean_stacks()
        python_code = translating_nodes.trans(
            parsed)  # syntax tree to python code
        cache[cp_hash] = {
            'compilation_plan': compilation_plan,
            'proto_python_code': python_code,
        }

    python_code = match_increaser_str.wrap_up(python_code)
    python_code = match_increaser_num.wrap_up(python_code)

    return HEADER + python_code
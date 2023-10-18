def translate_js(js, HEADER=DEFAULT_HEADER, use_compilation_plan=False):
    """js has to be a javascript source code.
       returns equivalent python code."""
    if use_compilation_plan and not '//' in js and not '/*' in js:
        return translate_js_with_compilation_plan(js, HEADER=HEADER)
    parser = pyjsparser.PyJsParser()
    parsed = parser.parse(js)  # js to esprima syntax tree
    # Another way of doing that would be with my auto esprima translation but its much slower and causes import problems:
    # parsed = esprima.parse(js).to_dict()
    translating_nodes.clean_stacks()
    return HEADER + translating_nodes.trans(
        parsed)
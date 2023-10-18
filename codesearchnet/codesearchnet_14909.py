def quick_doc(request_data):
    """
    Worker that returns the documentation of the symbol under cursor.
    """
    code = request_data['code']
    line = request_data['line'] + 1
    column = request_data['column']
    path = request_data['path']
    # encoding = 'utf-8'
    encoding = 'utf-8'
    script = jedi.Script(code, line, column, path, encoding)
    try:
        definitions = script.goto_definitions()
    except jedi.NotFoundError:
        return []
    else:
        ret_val = [d.docstring() for d in definitions]
        return ret_val
def goto_assignments(request_data):
    """
    Go to assignements worker.
    """
    code = request_data['code']
    line = request_data['line'] + 1
    column = request_data['column']
    path = request_data['path']
    # encoding = request_data['encoding']
    encoding = 'utf-8'
    script = jedi.Script(code, line, column, path, encoding)
    try:
        definitions = script.goto_assignments()
    except jedi.NotFoundError:
        pass
    else:
        ret_val = [(d.module_path, d.line - 1 if d.line else None,
                    d.column, d.full_name)
                   for d in definitions]
        return ret_val
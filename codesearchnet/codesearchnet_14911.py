def run_pyflakes(request_data):
    """
    Worker that run a frosted (the fork of pyflakes) code analysis on the
    current editor text.
    """
    global prev_results
    from pyflakes import checker
    import _ast
    WARNING = 1
    ERROR = 2
    ret_val = []
    code = request_data['code']
    path = request_data['path']
    encoding = request_data['encoding']
    if not encoding:
        encoding = 'utf-8'
    if not path:
        path = os.path.join(tempfile.gettempdir(), 'temp.py')
    if not code:
        return []
    else:
        # First, compile into an AST and handle syntax errors.
        try:
            tree = compile(code.encode(encoding), path, "exec",
                           _ast.PyCF_ONLY_AST)
        except SyntaxError as value:
            msg = '[pyFlakes] %s' % value.args[0]
            (lineno, offset, text) = value.lineno - 1, value.offset, value.text
            # If there's an encoding problem with the file, the text is None
            if text is None:
                # Avoid using msg, since for the only known case, it
                # contains a bogus message that claims the encoding the
                # file declared was unknown.s
                _logger().warning("[SyntaxError] %s: problem decoding source",
                                  path)
            else:
                ret_val.append((msg, ERROR, lineno))
        else:
            # Okay, it's syntactically valid.  Now check it.
            w = checker.Checker(tree, os.path.split(path)[1])
            w.messages.sort(key=lambda m: m.lineno)
            for message in w.messages:
                msg = "[pyFlakes] %s" % str(message).split(':')[-1].strip()
                line = message.lineno - 1
                status = WARNING \
                    if message.__class__ not in PYFLAKES_ERROR_MESSAGES \
                    else ERROR
                ret_val.append((msg, status, line))
    prev_results = ret_val
    return ret_val
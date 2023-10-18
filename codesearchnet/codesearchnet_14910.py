def run_pep8(request_data):
    """
    Worker that run the pep8 tool on the current editor text.

    :returns a list of tuples (msg, msg_type, line_number)
    """
    import pycodestyle
    from pyqode.python.backend.pep8utils import CustomChecker
    WARNING = 1
    code = request_data['code']
    path = request_data['path']
    max_line_length = request_data['max_line_length']
    ignore_rules = request_data['ignore_rules']
    ignore_rules += ['W291', 'W292', 'W293', 'W391']
    pycodestyle.MAX_LINE_LENGTH = max_line_length
    # setup our custom style guide with our custom checker which returns a list
    # of strings instread of spitting the results at stdout
    pep8style = pycodestyle.StyleGuide(parse_argv=False, config_file='',
                                       checker_class=CustomChecker)
    try:
        results = pep8style.input_file(path, lines=code.splitlines(True))
    except Exception:
        _logger().exception('Failed to run PEP8 analysis with data=%r'
                            % request_data)
        return []
    else:
        messages = []
        for line_number, offset, code, text, doc in results:
            if code in ignore_rules:
                continue
            messages.append(('[PEP8] %s: %s' % (code, text), WARNING,
                             line_number - 1))
        return messages
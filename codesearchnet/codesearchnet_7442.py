def eval_environ(value):
    """Evaluate environment markers."""
    def eval_environ_str(value):
        parts = value.split(';')
        if len(parts) < 2:
            return value
        expr = parts[1].lstrip()
        if not re.match("^((\\w+(\\.\\w+)?|'.*?'|\".*?\")\\s+"
                        '(in|==|!=|not in)\\s+'
                        "(\\w+(\\.\\w+)?|'.*?'|\".*?\")"
                        '(\\s+(or|and)\\s+)?)+$', expr):
            raise ValueError('bad environment marker: %r' % expr)
        expr = re.sub(r"(platform\.\w+)", r"\1()", expr)
        return parts[0] if eval(expr) else ''

    if isinstance(value, list):
        new_value = []
        for element in value:
            element = eval_environ_str(element)
            if element:
                new_value.append(element)
    elif isinstance(value, str):
        new_value = eval_environ_str(value)
    else:
        new_value = value

    return new_value
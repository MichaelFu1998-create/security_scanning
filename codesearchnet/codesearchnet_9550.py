def _filter_by_zoom(element=None, conf_string=None, zoom=None):
    """Return element only if zoom condition matches with config string."""
    for op_str, op_func in [
        # order of operators is important:
        # prematurely return in cases of "<=" or ">=", otherwise
        # _strip_zoom() cannot parse config strings starting with "<"
        # or ">"
        ("=", operator.eq),
        ("<=", operator.le),
        (">=", operator.ge),
        ("<", operator.lt),
        (">", operator.gt),
    ]:
        if conf_string.startswith(op_str):
            return element if op_func(zoom, _strip_zoom(conf_string, op_str)) else None
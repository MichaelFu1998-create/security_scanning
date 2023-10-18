def load_if(s):
    """Load either a filename, or a string representation of yml/json."""
    is_data_file = s.endswith('.json') or s.endswith('.yml')
    return load(s) if is_data_file else loads(s)
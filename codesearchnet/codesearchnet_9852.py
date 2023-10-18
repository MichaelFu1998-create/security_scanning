def is_safe_path(path):
    """Check if path is safe and allowed.
    """
    contains_windows_var = lambda val: re.match(r'%.+%', val)
    contains_posix_var = lambda val: re.match(r'\$.+', val)

    unsafeness_conditions = [
        os.path.isabs(path),
        ('..%s' % os.path.sep) in path,
        path.startswith('~'),
        os.path.expandvars(path) != path,
        contains_windows_var(path),
        contains_posix_var(path),
    ]

    return not any(unsafeness_conditions)
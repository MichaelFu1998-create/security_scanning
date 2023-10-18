def load_module(full_path):
    """
    Load module from full path
    Args:
        full_path: module full path name
    Returns:
        python module
    References:
        https://stackoverflow.com/a/67692/1332656
    Examples:
        >>> import os
        >>>
        >>> cur_file = os.path.abspath(__file__).replace('\\\\', '/')
        >>> cur_path = '/'.join(cur_file.split('/')[:-1])
        >>> load_module(f'{cur_path}/timezone.py').__name__
        'timezone'
        >>> load_module(f'{cur_path}/timezone.pyc')
        Traceback (most recent call last):
        ImportError: not a python file: timezone.pyc
    """
    from importlib import util

    file_name = full_path.replace('\\', '/').split('/')[-1]
    if file_name[-3:] != '.py':
        raise ImportError(f'not a python file: {file_name}')
    module_name = file_name[:-3]

    spec = util.spec_from_file_location(name=module_name, location=full_path)
    module = util.module_from_spec(spec=spec)
    spec.loader.exec_module(module=module)

    return module
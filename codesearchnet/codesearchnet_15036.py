def add_dir2pypath(path):
    """Add given directory to PYTHONPATH, e.g. for pylint."""
    py_path = os.environ.get('PYTHONPATH', '')
    if path not in py_path.split(os.pathsep):
        py_path = ''.join([path, os.pathsep if py_path else '', py_path])
        os.environ['PYTHONPATH'] = py_path
def is_venv(directory, executable='python'):
    """
    :param directory: base directory of python environment
    """
    path=os.path.join(directory, 'bin', executable)
    return os.path.isfile(path)
def get_project_root():
    """ Determine location of `tasks.py`."""
    try:
        tasks_py = sys.modules['tasks']
    except KeyError:
        return None
    else:
        return os.path.abspath(os.path.dirname(tasks_py.__file__))
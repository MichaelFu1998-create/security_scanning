def validate_project(project_name):
    """
    Check the defined project name against keywords, builtins and existing
    modules to avoid name clashing
    """
    if '-' in project_name:
        return None
    if keyword.iskeyword(project_name):
        return None
    if project_name in dir(__builtins__):
        return None
    try:
        __import__(project_name)
        return None
    except ImportError:
        return project_name
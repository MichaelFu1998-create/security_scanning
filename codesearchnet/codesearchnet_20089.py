def get_app_locations():
    """
    Returns list of paths to tested apps
    """
    return [os.path.dirname(os.path.normpath(import_module(app_name).__file__))
            for app_name in PROJECT_APPS]
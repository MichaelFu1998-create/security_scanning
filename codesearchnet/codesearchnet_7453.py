def set_directory(path=None):
    """Set LanguageTool directory."""
    old_path = get_directory()
    terminate_server()
    cache.clear()
    if path:
        cache['language_check_dir'] = path
        try:
            get_jar_info()
        except Error:
            cache['language_check_dir'] = old_path
            raise
def get_same_container_repos(app_or_library_name):
    """Given the name of an app or library, returns all repos that are guaranteed
    to live in the same container"""
    specs = get_expanded_libs_specs()
    spec = specs.get_app_or_lib(app_or_library_name)
    return get_same_container_repos_from_spec(spec)
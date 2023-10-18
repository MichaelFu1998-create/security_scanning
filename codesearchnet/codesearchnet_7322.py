def get_same_container_repos_from_spec(app_or_library_spec):
    """Given the spec of an app or library, returns all repos that are guaranteed
    to live in the same container"""
    repos = set()
    app_or_lib_repo = get_repo_of_app_or_library(app_or_library_spec.name)
    if app_or_lib_repo is not None:
        repos.add(app_or_lib_repo)
    for dependent_name in app_or_library_spec['depends']['libs']:
        repos.add(get_repo_of_app_or_library(dependent_name))
    return repos
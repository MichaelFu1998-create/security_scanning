def get_repo_of_app_or_library(app_or_library_name):
    """ This function takes an app or library name and will return the corresponding repo
    for that app or library"""
    specs = get_specs()
    repo_name = specs.get_app_or_lib(app_or_library_name)['repo']
    if not repo_name:
        return None
    return Repo(repo_name)
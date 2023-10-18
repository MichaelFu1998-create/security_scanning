def annotate_metadata_dependencies(repo):
    """
    Collect information from the dependent repo's
    """

    options = repo.options

    if 'dependencies' not in options:
        print("No dependencies")
        return []

    repos = []
    dependent_repos = options['dependencies']
    for d in dependent_repos:
        if "/" not in d:
            print("Invalid dependency specification")
        (username, reponame) = d.split("/")
        try:
            repos.append(repo.manager.lookup(username, reponame))
        except:
            print("Repository does not exist. Please create one", d)

    package = repo.package
    package['dependencies'] = []
    for r in repos:
        package['dependencies'].append({
            'username': r.username,
            'reponame': r.reponame,
            })
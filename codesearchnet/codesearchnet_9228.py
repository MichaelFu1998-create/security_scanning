def compose_git(projects, data):
    """ Compose projects.json for git

    We need to replace '/c/' by '/gitroot/' for instance

    change: 'http://git.eclipse.org/c/xwt/org.eclipse.xwt.git'
    to: 'http://git.eclipse.org/gitroot/xwt/org.eclipse.xwt.git'

    :param projects: projects.json
    :param data: eclipse JSON
    :return: projects.json with git
    """
    for p in [project for project in data if len(data[project]['source_repo']) > 0]:
        repos = []
        for url in data[p]['source_repo']:
            if len(url['url'].split()) > 1:  # Error at upstream the project 'tools.corrosion'
                repo = url['url'].split()[1].replace('/c/', '/gitroot/')
            else:
                repo = url['url'].replace('/c/', '/gitroot/')

            if repo not in repos:
                repos.append(repo)

        projects[p]['git'] = repos

    return projects
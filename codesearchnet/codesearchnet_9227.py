def compose_gerrit(projects):
    """ Compose projects.json for gerrit, but using the git lists

    change: 'http://git.eclipse.org/gitroot/xwt/org.eclipse.xwt.git'
    to: 'git.eclipse.org_xwt/org.eclipse.xwt

    :param projects: projects.json
    :return: projects.json with gerrit
    """
    git_projects = [project for project in projects if 'git' in projects[project]]
    for project in git_projects:
        repos = [repo for repo in projects[project]['git'] if 'gitroot' in repo]
        if len(repos) > 0:
            projects[project]['gerrit'] = []
        for repo in repos:
            gerrit_project = repo.replace("http://git.eclipse.org/gitroot/", "")
            gerrit_project = gerrit_project.replace(".git", "")
            projects[project]['gerrit'].append("git.eclipse.org_" + gerrit_project)

    return projects
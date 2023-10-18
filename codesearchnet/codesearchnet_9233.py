def compose_projects_json(projects, data):
    """ Compose projects.json with all data sources

    :param projects: projects.json
    :param data: eclipse JSON
    :return: projects.json with all data sources
    """
    projects = compose_git(projects, data)
    projects = compose_mailing_lists(projects, data)
    projects = compose_bugzilla(projects, data)
    projects = compose_github(projects, data)
    projects = compose_gerrit(projects)
    projects = compose_mbox(projects)

    return projects
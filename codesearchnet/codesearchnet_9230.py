def compose_github(projects, data):
    """ Compose projects.json for github

    :param projects: projects.json
    :param data: eclipse JSON
    :return: projects.json with github
    """
    for p in [project for project in data if len(data[project]['github_repos']) > 0]:
        if 'github' not in projects[p]:
            projects[p]['github'] = []

        urls = [url['url'] for url in data[p]['github_repos'] if
                url['url'] not in projects[p]['github']]
        projects[p]['github'] += urls

    return projects
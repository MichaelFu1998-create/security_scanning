def compose_bugzilla(projects, data):
    """ Compose projects.json for bugzilla

    :param projects: projects.json
    :param data: eclipse JSON
    :return: projects.json with bugzilla
    """
    for p in [project for project in data if len(data[project]['bugzilla']) > 0]:
        if 'bugzilla' not in projects[p]:
            projects[p]['bugzilla'] = []

        urls = [url['query_url'] for url in data[p]['bugzilla'] if
                url['query_url'] not in projects[p]['bugzilla']]
        projects[p]['bugzilla'] += urls

    return projects
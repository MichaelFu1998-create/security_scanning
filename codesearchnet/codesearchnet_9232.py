def compose_title(projects, data):
    """ Compose the projects JSON file only with the projects name

    :param projects: projects.json
    :param data: eclipse JSON with the origin format
    :return: projects.json with titles
    """
    for project in data:
        projects[project] = {
            'meta': {
                'title': data[project]['title']
            }
        }
    return projects
def compose_mailing_lists(projects, data):
    """ Compose projects.json for mailing lists

    At upstream has two different key for mailing list: 'mailings_lists' and 'dev_list'
    The key 'mailing_lists' is an array with mailing lists
    The key 'dev_list' is a dict with only one mailing list

    :param projects: projects.json
    :param data: eclipse JSON
    :return: projects.json with mailing_lists
    """
    for p in [project for project in data if len(data[project]['mailing_lists']) > 0]:
        if 'mailing_lists' not in projects[p]:
            projects[p]['mailing_lists'] = []

        urls = [url['url'].replace('mailto:', '') for url in data[p]['mailing_lists'] if
                url['url'] not in projects[p]['mailing_lists']]
        projects[p]['mailing_lists'] += urls

    for p in [project for project in data if len(data[project]['dev_list']) > 0]:
        if 'mailing_lists' not in projects[p]:
            projects[p]['mailing_lists'] = []

        mailing_list = data[p]['dev_list']['url'].replace('mailto:', '')
        projects[p]['mailing_lists'].append(mailing_list)

    return projects
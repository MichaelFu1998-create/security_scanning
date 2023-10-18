def create_query(section):
    """
        Creates a search query based on the section of the config file.
    """
    query = {}

    if 'ports' in section:
        query['ports'] = [section['ports']]
    if 'up' in section:
        query['up'] = bool(section['up'])
    if 'search' in section:
        query['search'] = [section['search']]
    if 'tags' in section:
        query['tags'] = [section['tags']]
    if 'groups' in section:
        query['groups'] = [section['groups']]

    return query
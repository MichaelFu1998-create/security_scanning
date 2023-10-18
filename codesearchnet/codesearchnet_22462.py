def create_tree(endpoints):
    """
    Creates the Trello endpoint tree.

    >>> r = {'1': { \
                 'actions': {'METHODS': {'GET'}}, \
                 'boards': { \
                     'members': {'METHODS': {'DELETE'}}}} \
            }
    >>> r == create_tree([ \
                 'GET /1/actions/[idAction]', \
                 'DELETE /1/boards/[board_id]/members/[idMember]'])
    True

    """
    tree = {}

    for method, url, doc in endpoints:
        path = [p for p in url.strip('/').split('/')]
        here = tree

        # First element (API Version).
        version = path[0]
        here.setdefault(version, {})
        here = here[version]

        # The rest of elements of the URL.
        for p in path[1:]:
            part = _camelcase_to_underscore(p)
            here.setdefault(part, {})
            here = here[part]

        # Allowed HTTP methods.
        if not 'METHODS' in here:
            here['METHODS'] = [[method, doc]]
        else:
            if not method in here['METHODS']:
                here['METHODS'].append([method, doc])

    return tree
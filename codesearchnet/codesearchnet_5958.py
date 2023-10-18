def iter_project(projects, key_file=None):
    """
    Call decorated function for each item in project list.

    Note: the function 'decorated' is expected to return a value plus a dictionary of exceptions.

    If item in list is a dictionary, we look for a 'project' and 'key_file' entry, respectively.
    If item in list is of type string_types, we assume it is the project string. Default credentials
    will be used by the underlying client library.

    :param projects: list of project strings or list of dictionaries
                     Example: {'project':..., 'keyfile':...}. Required.
    :type projects: ``list`` of ``str`` or ``list`` of ``dict``

    :param key_file: path on disk to keyfile, for use with all projects
    :type key_file: ``str``

    :returns: tuple containing a list of function output and an exceptions map
    :rtype: ``tuple of ``list``, ``dict``
    """

    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            item_list = []
            exception_map = {}
            for project in projects:
                if isinstance(project, string_types):
                    kwargs['project'] = project
                    if key_file:
                        kwargs['key_file'] = key_file
                elif isinstance(project, dict):
                    kwargs['project'] = project['project']
                    kwargs['key_file'] = project['key_file']
                itm, exc = func(*args, **kwargs)
                item_list.extend(itm)
                exception_map.update(exc)
            return (item_list, exception_map)

        return decorated_function

    return decorator
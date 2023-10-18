def create_project(name, short_name, description):
    """Create a project.

    :param name: PYBOSSA Project Name
    :type name: string
    :param short_name: PYBOSSA Project short name or slug
    :type short_name: string
    :param description: PYBOSSA Project description
    :type decription: string
    :returns: True -- the response status code

    """
    try:
        project = dict(name=name, short_name=short_name,
                       description=description)
        res = _pybossa_req('post', 'project', payload=project)
        if res.get('id'):
            return Project(res)
        else:
            return res
    except:  # pragma: no cover
        raise
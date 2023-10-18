def get_project(project_id):
    """Return a PYBOSSA Project for the project_id.

    :param project_id: PYBOSSA Project ID
    :type project_id: integer
    :rtype: PYBOSSA Project
    :returns: A PYBOSSA Project object

    """
    try:
        res = _pybossa_req('get', 'project', project_id)
        if res.get('id'):
            return Project(res)
        else:
            return res
    except:  # pragma: no cover
        raise
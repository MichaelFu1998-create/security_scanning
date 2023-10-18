def update_project(project):
    """Update a project instance.

    :param project: PYBOSSA project
    :type project: PYBOSSA Project
    :returns: True -- the response status code

    """
    try:
        project_id = project.id
        project = _forbidden_attributes(project)
        res = _pybossa_req('put', 'project', project_id, payload=project.data)
        if res.get('id'):
            return Project(res)
        else:
            return res
    except:  # pragma: no cover
        raise
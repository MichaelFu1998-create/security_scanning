def delete_project(project_id):
    """Delete a Project with id = project_id.

    :param project_id: PYBOSSA Project ID
    :type project_id: integer
    :returns: True -- the response status code

    """
    try:
        res = _pybossa_req('delete', 'project', project_id)
        if type(res).__name__ == 'bool':
            return True
        else:
            return res
    except:  # pragma: no cover
        raise
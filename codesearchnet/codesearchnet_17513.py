def find_helping_materials(project_id, **kwargs):
    """Return a list of matched helping materials for a given project ID.

    :param project_id: PYBOSSA Project ID
    :type project_id: integer
    :param kwargs: PYBOSSA HelpingMaterial members
    :type info: dict
    :rtype: list
    :returns: A list of helping materials that match the kwargs

    """
    try:
        kwargs['project_id'] = project_id
        res = _pybossa_req('get', 'helpingmaterial', params=kwargs)
        if type(res).__name__ == 'list':
            return [HelpingMaterial(helping) for helping in res]
        else:
            return res
    except:  # pragma: no cover
        raise
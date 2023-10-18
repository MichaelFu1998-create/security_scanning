def update_helping_material(helpingmaterial):
    """Update a helping material for a given helping material ID.

    :param helpingmaterial: PYBOSSA helping material

    """
    try:
        helpingmaterial_id = helpingmaterial.id
        helpingmaterial = _forbidden_attributes(helpingmaterial)
        res = _pybossa_req('put', 'helpingmaterial',
                           helpingmaterial_id, payload=helpingmaterial.data)
        if res.get('id'):
            return HelpingMaterial(res)
        else:
            return res
    except:  # pragma: no cover
        raise
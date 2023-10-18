def update_category(category):
    """Update a Category instance.

    :param category: PYBOSSA Category
    :type category: PYBOSSA Category
    :returns: True -- the response status code

    """
    try:
        res = _pybossa_req('put', 'category',
                           category.id, payload=category.data)
        if res.get('id'):
            return Category(res)
        else:
            return res
    except:  # pragma: no cover
        raise
def get_category(category_id):
    """Return a PYBOSSA Category for the category_id.

    :param category_id: PYBOSSA Category ID
    :type category_id: integer
    :rtype: PYBOSSA Category
    :returns: A PYBOSSA Category object

    """
    try:
        res = _pybossa_req('get', 'category', category_id)
        if res.get('id'):
            return Category(res)
        else:
            return res
    except:  # pragma: no cover
        raise
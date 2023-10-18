def create_category(name, description):
    """Create a Category.

    :param name: PYBOSSA Category Name
    :type name: string
    :param description: PYBOSSA Category description
    :type decription: string
    :returns: True -- the response status code
    """
    try:
        category = dict(name=name, short_name=name.lower().replace(" ", ""),
                        description=description)
        res = _pybossa_req('post', 'category', payload=category)
        if res.get('id'):
            return Category(res)
        else:
            return res
    except:  # pragma: no cover
        raise
def delete_category(category_id):
    """Delete a Category with id = category_id.

    :param category_id: PYBOSSA Category ID
    :type category_id: integer
    :returns: True -- the response status code

    """
    try:
        res = _pybossa_req('delete', 'category', category_id)
        if type(res).__name__ == 'bool':
            return True
        else:
            return res
    except:  # pragma: no cover
        raise
def update_result(result):
    """Update a result for a given result ID.

    :param result: PYBOSSA result

    """
    try:
        result_id = result.id
        result = _forbidden_attributes(result)
        res = _pybossa_req('put', 'result', result_id, payload=result.data)
        if res.get('id'):
            return Result(res)
        else:
            return res
    except:  # pragma: no cover
        raise
def to_dict_list(mystr):
    """
    Translate a string representation of a Bloomberg Open API Request/Response
    into a list of dictionaries.return

    Parameters
    ----------
    mystr: str
        A string representation of one or more blpapi.request.Request or
        blp.message.Message, these should be '\\n' seperated
    """
    res = _parse(mystr)
    dicts = []
    for res_dict in res:
        dicts.append(res_dict.asDict())
    return dicts
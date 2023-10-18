def _to_string(data):
    """ Convert to string all values in `data`.

    Parameters
    ----------
    data: dict[str]->object

    Returns
    -------
    string_data: dict[str]->str
    """
    sdata = data.copy()
    for k, v in data.items():
        if isinstance(v, datetime):
            sdata[k] = timestamp_to_date_str(v)

        elif not isinstance(v, (string_types, float, int)):
            sdata[k] = str(v)

    return sdata
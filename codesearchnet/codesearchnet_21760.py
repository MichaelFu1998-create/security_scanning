def decode_jsonld(jsonld_text):
    """Decode a JSON-LD dataset, including decoding datetime
    strings into `datetime.datetime` objects.

    Parameters
    ----------
    encoded_dataset : `str`
        The JSON-LD dataset encoded as a string.

    Returns
    -------
    jsonld_dataset : `dict`
        A JSON-LD dataset.

    Examples
    --------

    >>> doc = '{"dt": "2018-01-01T12:00:00Z"}'
    >>> decode_jsonld(doc)
    {'dt': datetime.datetime(2018, 1, 1, 12, 0, tzinfo=datetime.timezone.utc)}
    """
    decoder = json.JSONDecoder(object_pairs_hook=_decode_object_pairs)
    return decoder.decode(jsonld_text)
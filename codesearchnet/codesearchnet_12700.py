def _query_iedb(request_values, url):
    """
    Call into IEDB's web API for MHC binding prediction using request dictionary
    with fields:
        - "method"
        - "length"
        - "sequence_text"
        - "allele"

    Parse the response into a DataFrame.
    """
    data = urlencode(request_values)
    req = Request(url, data.encode("ascii"))
    response = urlopen(req).read()
    return _parse_iedb_response(response)
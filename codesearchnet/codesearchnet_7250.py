def _parse_sid_response(res):
    """Parse response format for request for new channel SID.

    Example format (after parsing JS):
    [   [0,["c","SID_HERE","",8]],
        [1,[{"gsid":"GSESSIONID_HERE"}]]]

    Returns (SID, gsessionid) tuple.
    """
    res = json.loads(list(ChunkParser().get_chunks(res))[0])
    sid = res[0][1][1]
    gsessionid = res[1][1][0]['gsid']
    return (sid, gsessionid)
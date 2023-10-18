def gce_list(service=None, **kwargs):
    """General list function for the GCE service."""
    resp_list = []
    req = service.list(**kwargs)

    while req is not None:
        resp = req.execute()
        for item in resp.get('items', []):
            resp_list.append(item)
        req = service.list_next(previous_request=req, previous_response=resp)
    return resp_list
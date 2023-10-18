def gce_list_aggregated(service=None, key_name='name', **kwargs):
    """General aggregated list function for the GCE service."""
    resp_list = []
    req = service.aggregatedList(**kwargs)

    while req is not None:
        resp = req.execute()
        for location, item in resp['items'].items():
            if key_name in item:
                resp_list.extend(item[key_name])

        req = service.aggregatedList_next(previous_request=req,
                                          previous_response=resp)
    return resp_list
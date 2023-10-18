def service_list(service=None, key_name=None, **kwargs):
    """General list function for Google APIs."""
    resp_list = []
    req = service.list(**kwargs)

    while req is not None:
        resp = req.execute()
        if key_name and key_name in resp:
            resp_list.extend(resp[key_name])
        else:
            resp_list.append(resp)
        # Not all list calls have a list_next
        if hasattr(service, 'list_next'):
            req = service.list_next(previous_request=req,
                                    previous_response=resp)
        else:
            req = None
    return resp_list
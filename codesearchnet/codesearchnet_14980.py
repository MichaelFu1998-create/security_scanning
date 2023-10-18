def owsproxy(request):
    """
    TODO: use ows exceptions
    """
    try:
        service_name = request.matchdict.get('service_name')
        extra_path = request.matchdict.get('extra_path')
        store = servicestore_factory(request.registry)
        service = store.fetch_by_name(service_name)
    except Exception as err:
        # TODO: Store impl should raise appropriate exception like not authorized
        return OWSAccessFailed("Could not find service {0} : {1}.".format(service_name, err.message))
    else:
        return _send_request(request, service, extra_path, request_params=request.query_string)
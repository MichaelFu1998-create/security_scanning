def adsAddRoute(net_id, ip_address):
    # type: (SAmsNetId, str) -> None
    """Establish a new route in the AMS Router.

    :param pyads.structs.SAmsNetId net_id: net id of routing endpoint
    :param str ip_address: ip address of the routing endpoint

    """
    add_route = _adsDLL.AdsAddRoute
    add_route.restype = ctypes.c_long

    # Convert ip address to bytes (PY3) and get pointer.
    ip_address_p = ctypes.c_char_p(ip_address.encode("utf-8"))

    error_code = add_route(net_id, ip_address_p)

    if error_code:
        raise ADSError(error_code)
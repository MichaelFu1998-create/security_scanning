def autodetect_url():
    """
    Try to autodetect the base URL of the router SOAP service.

    Returns None if it can't be found.
    """
    for url in ["http://routerlogin.net:5000", "https://routerlogin.net",
                "http://routerlogin.net"]:
        try:
            r = requests.get(url + "/soap/server_sa/",
                             headers=_get_soap_headers("Test:1", "test"),
                             verify=False)
            if r.status_code == 200:
                return url
        except requests.exceptions.RequestException:
            pass

    return None
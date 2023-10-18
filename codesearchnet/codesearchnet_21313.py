def check_service(service):
    """
        Connect to a service to see if it is a http or https server.
    """
    # Try HTTP
    service.add_tag('header_scan')
    http = False
    try:
        result = requests.head('http://{}:{}'.format(service.address, service.port), timeout=1)
        print_success("Found http service on {}:{}".format(service.address, service.port))
        service.add_tag('http')
        http = True
        try:
            service.banner = result.headers['Server']
        except KeyError:
            pass
    except (ConnectionError, ConnectTimeout, ReadTimeout, Error):
        pass

    if not http:
        # Try HTTPS
        try:
            result = requests.head('https://{}:{}'.format(service.address, service.port), verify=False, timeout=3)
            service.add_tag('https')
            print_success("Found https service on {}:{}".format(service.address, service.port))
            try:
                service.banner = result.headers['Server']
            except KeyError:
                pass
        except (ConnectionError, ConnectTimeout, ReadTimeout, Error):
            pass
    service.save()
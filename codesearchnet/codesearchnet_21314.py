def main():
    """
        Retrieves services starts check_service in a gevent pool of 100.
    """
    search = ServiceSearch()
    services = search.get_services(up=True, tags=['!header_scan'])
    print_notification("Scanning {} services".format(len(services)))

    # Disable the insecure request warning
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    pool = Pool(100)
    count = 0
    for service in services:
        count += 1
        if count % 50 == 0:
            print_notification("Checking {}/{} services".format(count, len(services)))
        pool.spawn(check_service, service)

    pool.join()
    print_notification("Completed, 'http' tag added to services that respond to http, 'https' tag added to services that respond to https.")
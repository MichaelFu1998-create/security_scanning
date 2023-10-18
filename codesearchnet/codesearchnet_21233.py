def main():
    """
        Checks the arguments to brutefore and spawns greenlets to perform the bruteforcing.
    """
    services = ServiceSearch()
    argparse = services.argparser
    argparse.add_argument('-f', '--file', type=str, help="File")
    arguments = argparse.parse_args()

    if not arguments.file:
        print_error("Please provide a file with credentials seperated by ':'")
        sys.exit()

    services = services.get_services(search=["Tomcat"], up=True, tags=['!tomcat_brute'])

    credentials = []
    with open(arguments.file, 'r') as f:
        credentials = f.readlines()

    for service in services:
        print_notification("Checking ip:{} port {}".format(service.address, service.port))
        url = 'http://{}:{}/manager/html'
        gevent.spawn(brutefore_passwords, service.address, url.format(service.address, service.port), credentials, service)
        service.add_tag('tomcat_brute')
        service.update(tags=service.tags)

    gevent.wait()
    # TODO fix stats
    Logger().log("tomcat_brute", "Performed tomcat bruteforce scan", {'scanned_services': len(services)})
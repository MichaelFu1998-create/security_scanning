def get_reliabledictionary_list(client, application_name, service_name):
    """List existing reliable dictionaries.

    List existing reliable dictionaries and respective schema for given application and service.

    :param application_name: Name of the application.
    :type application_name: str
    :param service_name: Name of the service.
    :type service_name: str
    """
    cluster = Cluster.from_sfclient(client)
    service = cluster.get_application(application_name).get_service(service_name)
    for dictionary in service.get_dictionaries():
        print(dictionary.name)
def execute_reliabledictionary(client, application_name, service_name, input_file):
    """Execute create, update, delete operations on existing reliable dictionaries.

    carry out create, update and delete operations on existing reliable dictionaries for given application and service.

    :param application_name: Name of the application.
    :type application_name: str
    :param service_name: Name of the service.
    :type service_name: str
    :param output_file: input file with list of json to provide the operation information for reliable dictionaries.
    """

    cluster = Cluster.from_sfclient(client)
    service = cluster.get_application(application_name).get_service(service_name)

    # call get service with headers and params
    with open(input_file) as json_file:
        json_data = json.load(json_file)
        service.execute(json_data)
    return
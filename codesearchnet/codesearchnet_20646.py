def query_reliabledictionary(client, application_name, service_name, dictionary_name, query_string, partition_key=None, partition_id=None, output_file=None):
    """Query existing reliable dictionary.

    Query existing reliable dictionaries for given application and service.

    :param application_name: Name of the application.
    :type application_name: str
    :param service_name: Name of the service.
    :type service_name: str
    :param dictionary_name: Name of the reliable dictionary.
    :type dictionary_name: str
    :param query_string: An OData query string. For example $top=10. Check https://www.odata.org/documentation/ for more information.
    :type query_string: str
    :param partition_key: Optional partition key of the desired partition, either a string if named schema or int if Int64 schema
    :type partition_id: str
    :param partition_id: Optional partition GUID of the owning reliable dictionary.
    :type partition_id: str
    :param output_file: Optional file to save the schema.
    """
    cluster = Cluster.from_sfclient(client)
    dictionary = cluster.get_application(application_name).get_service(service_name).get_dictionary(dictionary_name)
    
    
    start = time.time()
    if (partition_id != None):
        result = dictionary.query(query_string, PartitionLookup.ID, partition_id)
    elif (partition_key != None):
        result = dictionary.query(query_string, PartitionLookup.KEY, partition_key)
    else:
        result = dictionary.query(query_string)
    
    if type(result) is str:
        print(result)
        return
    else:
        result = json.dumps(result.get("value"), indent=4)
    
    print("Query took " + str(time.time() - start) + " seconds")
    
    if (output_file == None):
        output_file = "{}-{}-{}-query-output.json".format(application_name, service_name, dictionary_name)
    
    with open(output_file, "w") as output:
        output.write(result)
    print()
    print('Printed output to: ' + output_file)
    print(result)
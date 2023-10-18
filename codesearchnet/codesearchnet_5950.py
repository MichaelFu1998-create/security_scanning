def get_client(service, service_type='client', **conn_args):
    """
    User function to get the correct client.

    Based on the GOOGLE_CLIENT_MAP dictionary, the return will be a cloud or general
    client that can interact with the desired service.

    :param service: GCP service to connect to. E.g. 'gce', 'iam'
    :type service: ``str``

    :param conn_args: Dictionary of connection arguments.  'project' is required.
                      'user_agent' can be specified and will be set in the client
                       returned.
    :type conn_args: ``dict``

    :return: client_details, client
    :rtype: ``tuple`` of ``dict``, ``object``
    """
    client_details = choose_client(service)
    user_agent = get_user_agent(**conn_args)
    if client_details:
        if client_details['client_type'] == 'cloud':
            client = get_gcp_client(
                mod_name=client_details['module_name'],
                pkg_name=conn_args.get('pkg_name', 'google.cloud'),
                key_file=conn_args.get('key_file', None),
                project=conn_args['project'], user_agent=user_agent)
        else:
            client = get_google_client(
                mod_name=client_details['module_name'],
                key_file=conn_args.get('key_file', None),
                user_agent=user_agent, api_version=conn_args.get('api_version', 'v1'))
    else:
        # There is no client known for this service. We can try the standard API.
        try:
            client = get_google_client(
                mod_name=service, key_file=conn_args.get('key_file', None),
                user_agent=user_agent, api_version=conn_args.get('api_version', 'v1'))
        except Exception as e:
            raise e

    return client_details, client
def parse_config_file():
    """
    Find the .splunk_logger config file in the current directory, or in the
    user's home and parse it. The one in the current directory has precedence.
    
    :return: A tuple with:
                - project_id
                - access_token
    """
    for filename in ('.splunk_logger', os.path.expanduser('~/.splunk_logger')):

        project_id, access_token, api_domain = _parse_config_file_impl(filename)

        if project_id is not None\
        and access_token is not None\
        and api_domain is not None:
            return project_id, access_token, api_domain

    else:
        return None, None, None
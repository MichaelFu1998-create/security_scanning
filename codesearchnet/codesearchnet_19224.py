def _parse_config_file_impl(filename):
    """
    Format for the file is:
    
         credentials:
             project_id: ...
             access_token: ...
             api_domain: ...
    
    :param filename: The filename to parse
    :return: A tuple with:
                - project_id
                - access_token
                - api_domain
    """
    try:
        doc = yaml.load(file(filename).read())
        
        project_id = doc["credentials"]["project_id"]
        access_token = doc["credentials"]["access_token"]
        api_domain = doc["credentials"]["api_domain"]
        
        return project_id, access_token, api_domain
    except:
        return None, None, None
def get_gcp_client(**kwargs):
    """Public GCP client builder."""
    return _gcp_client(project=kwargs['project'], mod_name=kwargs['mod_name'],
                       pkg_name=kwargs.get('pkg_name', 'google.cloud'),
                       key_file=kwargs.get('key_file', None),
                       http_auth=kwargs.get('http', None),
                       user_agent=kwargs.get('user_agent', None))
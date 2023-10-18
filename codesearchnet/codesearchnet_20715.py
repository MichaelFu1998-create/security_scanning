def set_aad_metadata(uri, resource, client):
    """Set AAD metadata."""
    set_config_value('authority_uri', uri)
    set_config_value('aad_resource', resource)
    set_config_value('aad_client', client)
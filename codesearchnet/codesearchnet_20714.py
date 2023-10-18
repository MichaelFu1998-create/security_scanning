def set_aad_cache(token, cache):
    """Set AAD token cache."""
    set_config_value('aad_token', jsonpickle.encode(token))
    set_config_value('aad_cache', jsonpickle.encode(cache))
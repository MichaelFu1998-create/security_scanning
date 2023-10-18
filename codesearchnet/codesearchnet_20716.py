def set_auth(pem=None, cert=None, key=None, aad=False):
    """Set certificate usage paths"""

    if any([cert, key]) and pem:
        raise ValueError('Cannot specify both pem and cert or key')

    if any([cert, key]) and not all([cert, key]):
        raise ValueError('Must specify both cert and key')

    if pem:
        set_config_value('security', 'pem')
        set_config_value('pem_path', pem)
    elif cert or key:
        set_config_value('security', 'cert')
        set_config_value('cert_path', cert)
        set_config_value('key_path', key)
    elif aad:
        set_config_value('security', 'aad')
    else:
        set_config_value('security', 'none')
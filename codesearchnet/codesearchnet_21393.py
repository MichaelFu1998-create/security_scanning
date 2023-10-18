def create_connection(conf):
    """
        Creates a connection based upon the given configuration object.
    """
    host_config = {}
    host_config['hosts'] = [conf.get('jackal', 'host')]
    if int(conf.get('jackal', 'use_ssl')):
        host_config['use_ssl'] = True
    if conf.get('jackal', 'ca_certs'):
        host_config['ca_certs'] = conf.get('jackal', 'ca_certs')
    if int(conf.get('jackal', 'client_certs')):
        host_config['client_cert'] = conf.get('jackal', 'client_cert')
        host_config['client_key'] = conf.get('jackal', 'client_key')

    # Disable hostname checking for now.
    host_config['ssl_assert_hostname'] = False

    connections.create_connection(**host_config)
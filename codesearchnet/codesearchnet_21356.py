def manual_configure():
    """
        Function to manually configure jackal.
    """
    print("Manual configuring jackal")
    mapping = { '1': 'y', '0': 'n'}
    config = Config()
    # Host
    host = input_with_default("What is the Elasticsearch host?", config.get('jackal', 'host'))
    config.set('jackal', 'host', host)

    # SSL
    if input_with_default("Use SSL?", mapping[config.get('jackal', 'use_ssl')]) == 'y':
        config.set('jackal', 'use_ssl', '1')
        if input_with_default("Setup custom server cert?", 'y') == 'y':
            ca_certs = input_with_default("Server certificate location?", config.get('jackal', 'ca_certs'))
            config.set('jackal', 'ca_certs', ca_certs)
        else:
            config.set('jackal', 'ca_certs', '')
    else:
        config.set('jackal', 'use_ssl', '0')

    if input_with_default("Setup client certificates?", mapping[config.get('jackal', 'client_certs')]) == 'y':
        config.set('jackal', 'client_certs', '1')
        client_cert = input_with_default("Client cert location?", config.get('jackal', 'client_cert'))
        config.set('jackal', 'client_cert', client_cert)
        client_key = input_with_default("Client key location?", config.get('jackal', 'client_key'))
        config.set('jackal', 'client_key', client_key)
    else:
        config.set('jackal', 'client_certs', '0')

    # Index
    index = input_with_default("What index prefix should jackal use?", config.get('jackal', 'index'))
    config.set('jackal', 'index', index)
    initialize_indices = (input_with_default("Do you want to initialize the indices?", 'y').lower() == 'y')

    # Nmap
    nmap_dir = input_with_default("What directory do you want to place the nmap results in?", config.get('nmap', 'directory'))
    if not os.path.exists(nmap_dir):
        os.makedirs(nmap_dir)
    config.set('nmap', 'directory', nmap_dir)
    nmap_options = input_with_default("What nmap options do you want to set for 'custom' (for example '-p 22,445')?", config.get('nmap', 'options'))
    config.set('nmap', 'options', nmap_options)

    # Nessus
    configure_nessus = (input_with_default("Do you want to setup nessus?", 'n').lower() == 'y')
    if configure_nessus:
        nessus_host = input_with_default("What is the nessus host?", config.get('nessus', 'host'))
        nessus_template = input_with_default("What template should jackal use?", config.get('nessus', 'template_name'))
        nessus_access = input_with_default("What api access key should jackal use?", config.get('nessus', 'access_key'))
        nessus_secret = input_with_default("What api secret key should jackal use?", config.get('nessus', 'secret_key'))
        config.set('nessus', 'host', nessus_host)
        config.set('nessus', 'template_name', nessus_template)
        config.set('nessus', 'access_key', nessus_access)
        config.set('nessus', 'secret_key', nessus_secret)

    # Named pipes
    configure_pipes = (input_with_default("Do you want to setup named pipes?", 'n').lower() == 'y')
    if configure_pipes:
        directory = input_with_default("What directory do you want to place the named pipes in?", config.get('pipes', 'directory'))
        config.set('pipes', 'directory', directory)
        config_file = input_with_default("What is the name of the named pipe config?", config.get('pipes', 'config_file'))
        config.set('pipes', 'config_file', config_file)
        if not os.path.exists(directory):
            create = (input_with_default("Do you want to create the directory?", 'n').lower() == 'y')
            if create:
                os.makedirs(directory)
        if not os.path.exists(os.path.join(config.config_dir, config_file)):
            f = open(os.path.join(config.config_dir, config_file), 'a')
            f.close()

    config.write_config(initialize_indices)
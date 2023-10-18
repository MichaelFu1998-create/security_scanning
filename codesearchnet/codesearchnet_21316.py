def nmap(nmap_args, ips):
    """
        Start an nmap process with the given args on the given ips.
    """
    config = Config()
    arguments = ['nmap', '-Pn']
    arguments.extend(ips)
    arguments.extend(nmap_args)
    output_file = ''
    now = datetime.datetime.now()
    if not '-oA' in nmap_args:
        output_name = 'nmap_jackal_{}'.format(now.strftime("%Y-%m-%d %H:%M"))
        path_name = os.path.join(config.get('nmap', 'directory'), output_name)
        print_notification("Writing output of nmap to {}".format(path_name))
        if not os.path.exists(config.get('nmap', 'directory')):
            os.makedirs(config.get('nmap', 'directory'))
        output_file = path_name + '.xml'
        arguments.extend(['-oA', path_name])
    else:
        output_file = nmap_args[nmap_args.index('-oA') + 1] + '.xml'

    print_notification("Starting nmap")
    subprocess.call(arguments)

    with open(output_file, 'r') as f:
        return f.read()
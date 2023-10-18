def cmd_status(opts):
    """Print status of containers and networks
    """
    config = load_config(opts.config)
    b = get_blockade(config, opts)
    containers = b.status()
    print_containers(containers, opts.json)
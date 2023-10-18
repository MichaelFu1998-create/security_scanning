def cmd_up(opts):
    """Start the containers and link them together
    """
    config = load_config(opts.config)
    b = get_blockade(config, opts)
    containers = b.create(verbose=opts.verbose, force=opts.force)
    print_containers(containers, opts.json)
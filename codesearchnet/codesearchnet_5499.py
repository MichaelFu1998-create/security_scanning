def cmd_add(opts):
    """Add one or more existing Docker containers to a Blockade group
    """
    config = load_config(opts.config)
    b = get_blockade(config, opts)
    b.add_container(opts.containers)
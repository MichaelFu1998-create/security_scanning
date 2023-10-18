def cmd_join(opts):
    """Restore full networking between containers
    """
    config = load_config(opts.config)
    b = get_blockade(config, opts)
    b.join()
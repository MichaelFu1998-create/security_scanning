def cmd_destroy(opts):
    """Destroy all containers and restore networks
    """
    config = load_config(opts.config)
    b = get_blockade(config, opts)
    b.destroy()
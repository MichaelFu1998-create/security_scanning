def cmd_logs(opts):
    """Fetch the logs of a container
    """
    config = load_config(opts.config)
    b = get_blockade(config, opts)
    puts(b.logs(opts.container).decode(encoding='UTF-8'))
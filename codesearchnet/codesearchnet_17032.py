def start_proxy(config):
    """
    Start the http proxy
    :param config:
    :return:
    """
    protector = Protector(config.rules, config.whitelist)
    protector_daemon = ProtectorDaemon(config=config, protector=protector)

    daemon = daemonocle.Daemon(
        pidfile=config.pidfile,
        detach=(not config.foreground),
        shutdown_callback=shutdown,
        worker=protector_daemon.run
    )
    daemon.do_action(config.command)
def main():
    """
    Setup consumer
    """
    config = loader.load_config()
    if config.version:
        show_version()
    if config.show_rules:
        show_rules()
    if not config.configfile and not (hasattr(config, "status") or hasattr(config, "stop")):
        show_configfile_warning()

    # Check if we have permissions to open the log file.
    check_write_permissions(config.logfile)
    start_proxy(config)
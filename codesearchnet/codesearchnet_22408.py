def main():
    """Register your own mode and handle method here."""
    plugin = Register()
    if plugin.args.option == 'sql':
        plugin.sql_handle()
    else:
        plugin.unknown("Unknown actions.")
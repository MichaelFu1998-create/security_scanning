def main():
    """Register your own mode and handle method here."""
    plugin = Register()
    if plugin.args.option == 'command':
        plugin.command_handle()
    else:
        plugin.unknown("Unknown actions.")
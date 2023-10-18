def main():
    """Register your own mode and handle method here."""
    plugin = Register()
    if plugin.args.option == 'filenumber':
        plugin.filenumber_handle()
    else:
        plugin.unknown("Unknown actions.")
def main():
    """Register your own mode and handle method here."""
    plugin = Register()
    if plugin.args.option == 'filenumber':
        plugin.filenumber_handle()
    elif plugin.args.option == 'fileage':
        plugin.fileage_handle()
    elif plugin.args.option == 'sqlserverlocks':
        plugin.sqlserverlocks_handle()
    else:
        plugin.unknown("Unknown actions.")
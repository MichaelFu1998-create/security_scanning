def main():
    """Register your own mode and handle method here."""
    plugin = Register()
    if plugin.args.option == 'sql':
        plugin.sql_handle()
    elif plugin.args.option == 'database-used':
        plugin.database_used_handle()
    elif plugin.args.option == 'databaselog-used':
        plugin.database_log_used_handle()
    else:
        plugin.unknown("Unknown actions.")
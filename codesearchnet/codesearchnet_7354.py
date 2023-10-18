def add_exports_for_repos(repos):
    """
    This function will add needed entries to /etc/exports.  It will not remove any
    entries from the file.  It will then restart the server if necessary
    """
    current_exports = _get_current_exports()
    needed_exports = _get_exports_for_repos(repos)

    if not needed_exports.difference(current_exports):
        if not _server_is_running():
            _restart_server()
        return

    _write_exports_config(current_exports.union(needed_exports))
    _restart_server()
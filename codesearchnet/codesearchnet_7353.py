def configure_nfs_server():
    """
    This function is used with `dusty up`.  It will check all active repos to see if
    they are exported.  If any are missing, it will replace current dusty exports with
    exports that are needed for currently active repos, and restart
    the nfs server
    """
    repos_for_export = get_all_repos(active_only=True, include_specs_repo=False)

    current_exports = _get_current_exports()
    needed_exports = _get_exports_for_repos(repos_for_export)

    _ensure_managed_repos_dir_exists()

    if not needed_exports.difference(current_exports):
        if not _server_is_running():
            _restart_server()
        return

    _write_exports_config(needed_exports)
    _restart_server()
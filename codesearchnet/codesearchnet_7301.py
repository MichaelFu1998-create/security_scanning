def restart_apps_or_services(app_or_service_names=None):
    """Restart any containers associated with Dusty, or associated with
    the provided app_or_service_names."""
    if app_or_service_names:
        log_to_client("Restarting the following apps or services: {}".format(', '.join(app_or_service_names)))
    else:
        log_to_client("Restarting all active containers associated with Dusty")

    if app_or_service_names:
        specs = spec_assembler.get_assembled_specs()
        specs_list = [specs['apps'][app_name] for app_name in app_or_service_names if app_name in specs['apps']]
        repos = set()
        for spec in specs_list:
            if spec['repo']:
                repos = repos.union(spec_assembler.get_same_container_repos_from_spec(spec))
        nfs.update_nfs_with_repos(repos)
    else:
        nfs.update_nfs_with_repos(spec_assembler.get_all_repos(active_only=True, include_specs_repo=False))
    compose.restart_running_services(app_or_service_names)
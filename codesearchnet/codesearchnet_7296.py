def update_managed_repos(force=False):
    """For any active, managed repos, update the Dusty-managed
    copy to bring it up to date with the latest master."""
    log_to_client('Pulling latest updates for all active managed repos:')
    update_specs_repo_and_known_hosts()
    repos_to_update = get_all_repos(active_only=True, include_specs_repo=False)
    with parallel_task_queue() as queue:
        log_to_client('Updating managed repos')
        for repo in repos_to_update:
            if not repo.is_overridden:
                repo.update_local_repo_async(queue, force=force)
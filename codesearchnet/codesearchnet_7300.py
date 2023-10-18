def stop_apps_or_services(app_or_service_names=None, rm_containers=False):
    """Stop any currently running Docker containers associated with
    Dusty, or associated with the provided apps_or_services. Does not remove
    the service's containers."""
    if app_or_service_names:
        log_to_client("Stopping the following apps or services: {}".format(', '.join(app_or_service_names)))
    else:
        log_to_client("Stopping all running containers associated with Dusty")

    compose.stop_running_services(app_or_service_names)
    if rm_containers:
        compose.rm_containers(app_or_service_names)
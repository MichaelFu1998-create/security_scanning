def _start_docker_vm():
    """Start the Dusty VM if it is not already running."""
    is_running = docker_vm_is_running()
    if not is_running:
        log_to_client('Starting docker-machine VM {}'.format(constants.VM_MACHINE_NAME))
        _apply_nat_dns_host_resolver()
        _apply_nat_net_less_greedy_subnet()
        check_and_log_output_and_error_demoted(['docker-machine', 'start', constants.VM_MACHINE_NAME], quiet_on_success=True)
    return is_running
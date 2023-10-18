def _init_docker_vm():
    """Initialize the Dusty VM if it does not already exist."""
    if not _dusty_vm_exists():
        log_to_client('Initializing new Dusty VM with Docker Machine')
        machine_options = ['--driver', 'virtualbox',
                           '--virtualbox-cpu-count', '-1',
                           '--virtualbox-boot2docker-url', constants.CONFIG_BOOT2DOCKER_URL,
                           '--virtualbox-memory', str(get_config_value(constants.CONFIG_VM_MEM_SIZE)),
                           '--virtualbox-hostonly-nictype', constants.VM_NIC_TYPE]
        check_call_demoted(['docker-machine', 'create'] + machine_options + [constants.VM_MACHINE_NAME],
                           redirect_stderr=True)
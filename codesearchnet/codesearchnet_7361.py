def _dusty_vm_exists():
    """We use VBox directly instead of Docker Machine because it
    shaves about 0.5 seconds off the runtime of this check."""
    existing_vms = check_output_demoted(['VBoxManage', 'list', 'vms'])
    for line in existing_vms.splitlines():
        if '"{}"'.format(constants.VM_MACHINE_NAME) in line:
            return True
    return False
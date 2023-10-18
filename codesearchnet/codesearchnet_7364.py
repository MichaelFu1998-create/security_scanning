def docker_vm_is_running():
    """Using VBoxManage is 0.5 seconds or so faster than Machine."""
    running_vms = check_output_demoted(['VBoxManage', 'list', 'runningvms'])
    for line in running_vms.splitlines():
        if '"{}"'.format(constants.VM_MACHINE_NAME) in line:
            return True
    return False
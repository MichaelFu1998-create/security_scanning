def _get_host_only_mac_address():
    """Returns the MAC address assigned to the host-only adapter,
    using output from VBoxManage. Returned MAC address has no colons
    and is lower-cased."""
    # Get the number of the host-only adapter
    vm_config = _get_vm_config()
    for line in vm_config:
        if line.startswith('hostonlyadapter'):
            adapter_number = int(line[15:16])
            break
    else:
        raise ValueError('No host-only adapter is defined for the Dusty VM')

    for line in vm_config:
        if line.startswith('macaddress{}'.format(adapter_number)):
            return line.split('=')[1].strip('"').lower()
    raise ValueError('Could not find MAC address for adapter number {}'.format(adapter_number))
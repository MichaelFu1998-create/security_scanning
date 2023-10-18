def _get_localhost_ssh_port():
    """Something in the VM chain, either VirtualBox or Machine, helpfully
    sets up localhost-to-VM forwarding on port 22. We can inspect this
    rule to determine the port on localhost which gets forwarded to
    22 in the VM."""
    for line in _get_vm_config():
        if line.startswith('Forwarding'):
            spec = line.split('=')[1].strip('"')
            name, protocol, host, host_port, target, target_port = spec.split(',')
            if name == 'ssh' and protocol == 'tcp' and target_port == '22':
                return host_port
    raise ValueError('Could not determine localhost port for SSH forwarding')
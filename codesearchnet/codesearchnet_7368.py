def _get_host_only_ip():
    """Determine the host-only IP of the Dusty VM through Virtualbox and SSH
    directly, bypassing Docker Machine. We do this because Docker Machine is
    much slower, taking about 600ms total. We are basically doing the same
    flow Docker Machine does in its own code."""
    mac = _get_host_only_mac_address()
    ip_addr_show = check_output_demoted(['ssh', '-o', 'StrictHostKeyChecking=no',
                                         '-o', 'UserKnownHostsFile=/dev/null',
                                         '-i', _vm_key_path(), '-p', _get_localhost_ssh_port(),
                                         'docker@127.0.0.1', 'ip addr show'])
    return _ip_for_mac_from_ip_addr_show(ip_addr_show, mac)
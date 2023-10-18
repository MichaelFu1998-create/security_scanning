def _build_ssh_command(conn_info, no_tunnel=False):
    """
    # TODO: Document clearly
    IndetityFile="~/.ssh/id_rsa"
    ProxyCommand="ssh -i ~/.ssh/id_rsa proxy_IP nc HOST_IP HOST_PORT"
    """
    command = ['ssh', '-i', conn_info['ssh_key_path'], conn_info['conn']]

    if conn_info.get('tunnel') and not no_tunnel:
        command.insert(1, conn_info.get('tunnel'))
        # Tunnel
        command.insert(1, '-L')
        # No shell
        command.insert(1, '-N')
    if conn_info.get('proxy'):
        command.extend(_build_proxy_command(conn_info))
    if conn_info.get('extend'):
        command.append(conn_info.get('extend'))
    return command
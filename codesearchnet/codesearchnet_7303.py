def _compose_dict_for_nginx(port_specs):
    """Return a dictionary containing the Compose spec required to run
    Dusty's nginx container used for host forwarding."""
    spec = {'image': constants.NGINX_IMAGE,
            'volumes': ['{}:{}'.format(constants.NGINX_CONFIG_DIR_IN_VM, constants.NGINX_CONFIG_DIR_IN_CONTAINER)],
            'command': 'nginx -g "daemon off;" -c /etc/nginx/conf.d/nginx.primary',
            'container_name': 'dusty_{}_1'.format(constants.DUSTY_NGINX_NAME)}
    all_host_ports = set([nginx_spec['host_port'] for nginx_spec in port_specs['nginx']])
    if all_host_ports:
        spec['ports'] = []
        for port in all_host_ports:
            spec['ports'].append('{0}:{0}'.format(port))
    return {constants.DUSTY_NGINX_NAME: spec}
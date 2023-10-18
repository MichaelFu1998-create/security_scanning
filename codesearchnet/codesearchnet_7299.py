def start_local_env(recreate_containers):
    """This command will use the compilers to get compose specs
    will pass those specs to the systems that need them. Those
    systems will in turn launch the services needed to make the
    local environment go."""

    assembled_spec = spec_assembler.get_assembled_specs()
    required_absent_assets = virtualbox.required_absent_assets(assembled_spec)
    if required_absent_assets:
        raise RuntimeError('Assets {} are specified as required but are not set. Set them with `dusty assets set`'.format(required_absent_assets))

    docker_ip = virtualbox.get_docker_vm_ip()

    # Stop will fail if we've never written a Composefile before
    if os.path.exists(constants.COMPOSEFILE_PATH):
        try:
            stop_apps_or_services(rm_containers=recreate_containers)
        except CalledProcessError as e:
            log_to_client("WARNING: docker-compose stop failed")
            log_to_client(str(e))

    daemon_warnings.clear_namespace('disk')
    df_info = virtualbox.get_docker_vm_disk_info(as_dict=True)
    if 'M' in df_info['free'] or 'K' in df_info['free']:
        warning_msg = 'VM is low on disk. Available disk: {}'.format(df_info['free'])
        daemon_warnings.warn('disk', warning_msg)
        log_to_client(warning_msg)

    log_to_client("Compiling together the assembled specs")
    active_repos = spec_assembler.get_all_repos(active_only=True, include_specs_repo=False)
    log_to_client("Compiling the port specs")
    port_spec = port_spec_compiler.get_port_spec_document(assembled_spec, docker_ip)
    log_to_client("Compiling the nginx config")
    docker_bridge_ip = virtualbox.get_docker_bridge_ip()
    nginx_config = nginx_compiler.get_nginx_configuration_spec(port_spec, docker_bridge_ip)
    log_to_client("Creating setup and script bash files")
    make_up_command_files(assembled_spec, port_spec)
    log_to_client("Compiling docker-compose config")
    compose_config = compose_compiler.get_compose_dict(assembled_spec, port_spec)

    log_to_client("Saving port forwarding to hosts file")
    hosts.update_hosts_file_from_port_spec(port_spec)
    log_to_client("Configuring NFS")
    nfs.configure_nfs()
    log_to_client("Saving updated nginx config to the VM")
    nginx.update_nginx_from_config(nginx_config)
    log_to_client("Saving Docker Compose config and starting all containers")
    compose.update_running_containers_from_spec(compose_config, recreate_containers=recreate_containers)

    log_to_client("Your local environment is now started!")
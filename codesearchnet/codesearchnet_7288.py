def update_nginx_from_config(nginx_config):
    """Write the given config to disk as a Dusty sub-config
    in the Nginx includes directory. Then, either start nginx
    or tell it to reload its config to pick up what we've
    just written."""
    logging.info('Updating nginx with new Dusty config')
    temp_dir = tempfile.mkdtemp()
    os.mkdir(os.path.join(temp_dir, 'html'))
    _write_nginx_config(constants.NGINX_BASE_CONFIG, os.path.join(temp_dir, constants.NGINX_PRIMARY_CONFIG_NAME))
    _write_nginx_config(nginx_config['http'], os.path.join(temp_dir, constants.NGINX_HTTP_CONFIG_NAME))
    _write_nginx_config(nginx_config['stream'], os.path.join(temp_dir, constants.NGINX_STREAM_CONFIG_NAME))
    _write_nginx_config(constants.NGINX_502_PAGE_HTML, os.path.join(temp_dir, 'html', constants.NGINX_502_PAGE_NAME))
    sync_local_path_to_vm(temp_dir, constants.NGINX_CONFIG_DIR_IN_VM)
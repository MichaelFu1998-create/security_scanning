def write_groovy_script_and_configs(
        filename, content, job_configs, view_configs=None):
    """Write out the groovy script and configs to file.

    This writes the reconfigure script to the file location
    and places the expanded configs in subdirectories 'view_configs' /
    'job_configs' that the script can then access when run.
    """
    with open(filename, 'w') as h:
        h.write(content)

    if view_configs:
        view_config_dir = os.path.join(os.path.dirname(filename), 'view_configs')
        if not os.path.isdir(view_config_dir):
            os.makedirs(view_config_dir)
        for config_name, config_body in view_configs.items():
            config_filename = os.path.join(view_config_dir, config_name)
            with open(config_filename, 'w') as config_fh:
                config_fh.write(config_body)

    job_config_dir = os.path.join(os.path.dirname(filename), 'job_configs')
    if not os.path.isdir(job_config_dir):
        os.makedirs(job_config_dir)
    # prefix each config file with a serial number to maintain order
    format_str = '%0' + str(len(str(len(job_configs)))) + 'd'
    i = 0
    for config_name, config_body in job_configs.items():
        i += 1
        config_filename = os.path.join(
            job_config_dir,
            format_str % i + ' ' + config_name)
        with open(config_filename, 'w') as config_fh:
            config_fh.write(config_body)
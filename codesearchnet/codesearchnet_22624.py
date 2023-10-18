def update_config(new_config):
    """ Update config options with the provided dictionary of options.
    """
    flask_app.base_config.update(new_config)

    # Check for changed working directory.
    if new_config.has_key('working_directory'):
        wd = os.path.abspath(new_config['working_directory'])
        if nbmanager.notebook_dir != wd:
            if not os.path.exists(wd):
                raise IOError('Path not found: %s' % wd)
            nbmanager.notebook_dir = wd
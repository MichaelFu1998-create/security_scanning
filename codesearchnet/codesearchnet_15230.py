def upload_theme():
    """ upload and/or update the theme with the current git state"""
    get_vars()
    with fab.settings():
        local_theme_path = path.abspath(
            path.join(fab.env['config_base'],
                fab.env.instance.config['local_theme_path']))
        rsync(
            '-av',
            '--delete',
            '%s/' % local_theme_path,
            '{{host_string}}:{themes_dir}/{ploy_theme_name}'.format(**AV)
        )
        briefkasten_ctl('restart')
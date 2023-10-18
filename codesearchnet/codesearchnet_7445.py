def cfg_to_args(config):
    """Compatibility helper to use setup.cfg in setup.py."""
    kwargs = {}
    opts_to_args = {
        'metadata': [
            ('name', 'name'),
            ('author', 'author'),
            ('author-email', 'author_email'),
            ('maintainer', 'maintainer'),
            ('maintainer-email', 'maintainer_email'),
            ('home-page', 'url'),
            ('summary', 'description'),
            ('description', 'long_description'),
            ('download-url', 'download_url'),
            ('classifier', 'classifiers'),
            ('platform', 'platforms'),
            ('license', 'license'),
            ('keywords', 'keywords'),
        ],
        'files': [
            ('packages_root', 'package_dir'),
            ('packages', 'packages'),
            ('modules', 'py_modules'),
            ('scripts', 'scripts'),
            ('package_data', 'package_data'),
            ('data_files', 'data_files'),
        ],
    }

    opts_to_args['metadata'].append(('requires-dist', 'install_requires'))
    if IS_PY2K and not which('3to2'):
        kwargs['setup_requires'] = ['3to2']
    kwargs['zip_safe'] = False

    for section in opts_to_args:
        for option, argname in opts_to_args[section]:
            value = get_cfg_value(config, section, option)
            if value:
                kwargs[argname] = value

    if 'long_description' not in kwargs:
        kwargs['long_description'] = read_description_file(config)

    if 'package_dir' in kwargs:
        kwargs['package_dir'] = {'': kwargs['package_dir']}

    if 'keywords' in kwargs:
        kwargs['keywords'] = split_elements(kwargs['keywords'])

    if 'package_data' in kwargs:
        kwargs['package_data'] = get_package_data(kwargs['package_data'])

    if 'data_files' in kwargs:
        kwargs['data_files'] = get_data_files(kwargs['data_files'])

    kwargs['version'] = get_version()

    if not IS_PY2K:
        kwargs['test_suite'] = 'test'

    return kwargs
def build(
    src, requirements=None, local_package=None,
    config_file='config.yaml', profile_name=None,
):
    """Builds the file bundle.

    :param str src:
       The path to your Lambda ready project (folder must contain a valid
        config.yaml and handler module (e.g.: service.py).
    :param str local_package:
        The path to a local package with should be included in the deploy as
        well (and/or is not available on PyPi)
    """
    # Load and parse the config file.
    path_to_config_file = os.path.join(src, config_file)
    cfg = read_cfg(path_to_config_file, profile_name)

    # Get the absolute path to the output directory and create it if it doesn't
    # already exist.
    dist_directory = cfg.get('dist_directory', 'dist')
    path_to_dist = os.path.join(src, dist_directory)
    mkdir(path_to_dist)

    # Combine the name of the Lambda function with the current timestamp to use
    # for the output filename.
    function_name = cfg.get('function_name')
    output_filename = '{0}-{1}.zip'.format(timestamp(), function_name)

    path_to_temp = mkdtemp(prefix='aws-lambda')
    pip_install_to_target(
        path_to_temp,
        requirements=requirements,
        local_package=local_package,
    )

    # Hack for Zope.
    if 'zope' in os.listdir(path_to_temp):
        print(
            'Zope packages detected; fixing Zope package paths to '
            'make them importable.',
        )
        # Touch.
        with open(os.path.join(path_to_temp, 'zope/__init__.py'), 'wb'):
            pass

    # Gracefully handle whether ".zip" was included in the filename or not.
    output_filename = (
        '{0}.zip'.format(output_filename)
        if not output_filename.endswith('.zip')
        else output_filename
    )

    # Allow definition of source code directories we want to build into our
    # zipped package.
    build_config = defaultdict(**cfg.get('build', {}))
    build_source_directories = build_config.get('source_directories', '')
    build_source_directories = (
        build_source_directories
        if build_source_directories is not None
        else ''
    )
    source_directories = [
        d.strip() for d in build_source_directories.split(',')
    ]

    files = []
    for filename in os.listdir(src):
        if os.path.isfile(filename):
            if filename == '.DS_Store':
                continue
            if filename == config_file:
                continue
            print('Bundling: %r' % filename)
            files.append(os.path.join(src, filename))
        elif os.path.isdir(filename) and filename in source_directories:
            print('Bundling directory: %r' % filename)
            files.append(os.path.join(src, filename))

    # "cd" into `temp_path` directory.
    os.chdir(path_to_temp)
    for f in files:
        if os.path.isfile(f):
            _, filename = os.path.split(f)

            # Copy handler file into root of the packages folder.
            copyfile(f, os.path.join(path_to_temp, filename))
            copystat(f, os.path.join(path_to_temp, filename))
        elif os.path.isdir(f):
            destination_folder = os.path.join(path_to_temp, f[len(src) + 1:])
            copytree(f, destination_folder)

    # Zip them together into a single file.
    # TODO: Delete temp directory created once the archive has been compiled.
    path_to_zip_file = archive('./', path_to_dist, output_filename)
    return path_to_zip_file
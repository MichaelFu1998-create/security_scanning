def upload(
        src, requirements=None, local_package=None,
        config_file='config.yaml', profile_name=None,
):
    """Uploads a new function to AWS S3.

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

    # Copy all the pip dependencies required to run your code into a temporary
    # folder then add the handler file in the root of this directory.
    # Zip the contents of this folder into a single file and output to the dist
    # directory.
    path_to_zip_file = build(
        src, config_file=config_file, requirements=requirements,
        local_package=local_package,
    )

    upload_s3(cfg, path_to_zip_file)
def create(
    mapchete_file,
    process_file,
    out_format,
    out_path=None,
    pyramid_type=None,
    force=False
):
    """Create an empty Mapchete and process file in a given directory."""
    if os.path.isfile(process_file) or os.path.isfile(mapchete_file):
        if not force:
            raise IOError("file(s) already exists")

    out_path = out_path if out_path else os.path.join(os.getcwd(), "output")

    # copy file template to target directory
    process_template = pkg_resources.resource_filename(
        "mapchete.static", "process_template.py"
    )
    process_file = os.path.join(os.getcwd(), process_file)
    copyfile(process_template, process_file)

    # modify and copy mapchete file template to target directory
    mapchete_template = pkg_resources.resource_filename(
        "mapchete.static", "mapchete_template.mapchete"
    )

    output_options = dict(
        format=out_format, path=out_path, **FORMAT_MANDATORY[out_format]
    )

    pyramid_options = {'grid': pyramid_type}

    substitute_elements = {
        'process_file': process_file,
        'output': dump({'output': output_options}, default_flow_style=False),
        'pyramid': dump({'pyramid': pyramid_options}, default_flow_style=False)
    }
    with open(mapchete_template, 'r') as config_template:
        config = Template(config_template.read())
        customized_config = config.substitute(substitute_elements)
    with open(mapchete_file, 'w') as target_config:
        target_config.write(customized_config)
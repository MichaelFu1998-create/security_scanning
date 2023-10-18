def show(dataset_uri):
    """Show the descriptive metadata in the readme."""
    try:
        dataset = dtoolcore.ProtoDataSet.from_uri(
            uri=dataset_uri,
            config_path=CONFIG_PATH
        )
    except dtoolcore.DtoolCoreTypeError:
        dataset = dtoolcore.DataSet.from_uri(
            uri=dataset_uri,
            config_path=CONFIG_PATH
        )
    readme_content = dataset.get_readme_content()
    click.secho(readme_content)
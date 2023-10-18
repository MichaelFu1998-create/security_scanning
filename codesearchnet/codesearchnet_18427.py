def name(dataset_uri, new_name):
    """
    Report / update the name of the dataset.

    It is only possible to update the name of a proto dataset,
    i.e. a dataset that has not yet been frozen.
    """
    if new_name != "":
        _validate_name(new_name)

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

        dataset.update_name(new_name)

    admin_metadata = dtoolcore._admin_metadata_from_uri(
        uri=dataset_uri,
        config_path=CONFIG_PATH
    )
    click.secho(admin_metadata["name"])
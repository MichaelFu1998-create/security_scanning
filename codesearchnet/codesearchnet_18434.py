def freeze(proto_dataset_uri):
    """Convert a proto dataset into a dataset.

    This step is carried out after all files have been added to the dataset.
    Freezing a dataset finalizes it with a stamp marking it as frozen.
    """
    proto_dataset = dtoolcore.ProtoDataSet.from_uri(
        uri=proto_dataset_uri,
        config_path=CONFIG_PATH
    )

    num_items = len(list(proto_dataset._identifiers()))
    max_files_limit = int(dtoolcore.utils.get_config_value(
        "DTOOL_MAX_FILES_LIMIT",
        CONFIG_PATH,
        10000
    ))
    assert isinstance(max_files_limit, int)
    if num_items > max_files_limit:
        click.secho(
            "Too many items ({} > {}) in proto dataset".format(
                num_items,
                max_files_limit
            ),
            fg="red"
        )
        click.secho("1. Consider splitting the dataset into smaller datasets")
        click.secho("2. Consider packaging small files using tar")
        click.secho("3. Increase the limit using the DTOOL_MAX_FILES_LIMIT")
        click.secho("   environment variable")
        sys.exit(2)

    handles = [h for h in proto_dataset._storage_broker.iter_item_handles()]
    for h in handles:
        if not valid_handle(h):
            click.secho(
                "Invalid item name: {}".format(h),
                fg="red"
            )
            click.secho("1. Consider renaming the item")
            click.secho("2. Consider removing the item")
            sys.exit(3)

    with click.progressbar(length=len(list(proto_dataset._identifiers())),
                           label="Generating manifest") as progressbar:
        try:
            proto_dataset.freeze(progressbar=progressbar)
        except dtoolcore.storagebroker.DiskStorageBrokerValidationWarning as e:
            click.secho("")
            click.secho(str(e), fg="red", nl=False)
            sys.exit(4)

    click.secho("Dataset frozen ", nl=False, fg="green")
    click.secho(proto_dataset_uri)
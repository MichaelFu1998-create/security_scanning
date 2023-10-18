def create(quiet, name, base_uri, symlink_path):
    """Create a proto dataset."""
    _validate_name(name)

    admin_metadata = dtoolcore.generate_admin_metadata(name)
    parsed_base_uri = dtoolcore.utils.generous_parse_uri(base_uri)

    if parsed_base_uri.scheme == "symlink":
        if symlink_path is None:
            raise click.UsageError("Need to specify symlink path using the -s/--symlink-path option")  # NOQA

    if symlink_path:
        base_uri = dtoolcore.utils.sanitise_uri(
            "symlink:" + parsed_base_uri.path
        )
        parsed_base_uri = dtoolcore.utils.generous_parse_uri(base_uri)

    # Create the dataset.
    proto_dataset = dtoolcore.generate_proto_dataset(
        admin_metadata=admin_metadata,
        base_uri=dtoolcore.utils.urlunparse(parsed_base_uri),
        config_path=CONFIG_PATH)

    # If we are creating a symlink dataset we need to set the symlink_path
    # attribute on the storage broker.
    if symlink_path:
        symlink_abspath = os.path.abspath(symlink_path)
        proto_dataset._storage_broker.symlink_path = symlink_abspath
    try:
        proto_dataset.create()
    except dtoolcore.storagebroker.StorageBrokerOSError as err:
        raise click.UsageError(str(err))

    proto_dataset.put_readme("")

    if quiet:
        click.secho(proto_dataset.uri)
    else:
        # Give the user some feedback and hints on what to do next.
        click.secho("Created proto dataset ", nl=False, fg="green")
        click.secho(proto_dataset.uri)
        click.secho("Next steps: ")

        step = 1

        if parsed_base_uri.scheme != "symlink":
            click.secho("{}. Add raw data, eg:".format(step))
            click.secho(
                "   dtool add item my_file.txt {}".format(proto_dataset.uri),
                fg="cyan")

            if parsed_base_uri.scheme == "file":
                # Find the abspath of the data directory for user feedback.
                data_path = proto_dataset._storage_broker._data_abspath
                click.secho("   Or use your system commands, e.g: ")
                click.secho(
                    "   mv my_data_directory {}/".format(data_path),
                    fg="cyan"
                )
            step = step + 1

        click.secho("{}. Add descriptive metadata, e.g: ".format(step))
        click.secho(
            "   dtool readme interactive {}".format(proto_dataset.uri),
            fg="cyan")
        step = step + 1

        click.secho(
            "{}. Convert the proto dataset into a dataset: ".format(step)
        )
        click.secho("   dtool freeze {}".format(proto_dataset.uri), fg="cyan")
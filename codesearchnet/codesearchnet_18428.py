def interactive(proto_dataset_uri):
    """Interactive prompting to populate the readme."""
    proto_dataset = dtoolcore.ProtoDataSet.from_uri(
        uri=proto_dataset_uri,
        config_path=CONFIG_PATH)

    # Create an CommentedMap representation of the yaml readme template.
    readme_template = _get_readme_template()
    yaml = YAML()
    yaml.explicit_start = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    descriptive_metadata = yaml.load(readme_template)

    descriptive_metadata = _prompt_for_values(descriptive_metadata)

    # Write out the descriptive metadata to the readme file.
    stream = StringIO()

    yaml.dump(descriptive_metadata, stream)

    proto_dataset.put_readme(stream.getvalue())

    click.secho("Updated readme ", fg="green")
    click.secho("To edit the readme using your default editor:")
    click.secho(
        "dtool readme edit {}".format(proto_dataset_uri),
        fg="cyan")
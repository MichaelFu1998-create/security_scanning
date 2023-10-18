def edit(dataset_uri):
    """Default editor updating of readme content.
    """
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

    try:
        # Python2 compatibility.
        readme_content = unicode(readme_content, "utf-8")
    except NameError:
        pass

    edited_content = click.edit(readme_content)
    if edited_content is not None:
        _validate_and_put_readme(dataset, edited_content)
        click.secho("Updated readme ", nl=False, fg="green")
    else:
        click.secho("Did not update readme ", nl=False, fg="red")
    click.secho(dataset_uri)
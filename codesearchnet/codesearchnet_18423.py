def publish(quiet, dataset_uri):
    """Enable HTTP access to a dataset.

    This only works on datasets in some systems. For example, datasets stored
    in AWS S3 object storage and Microsoft Azure Storage can be published as
    datasets accessible over HTTP. A published dataset is world readable.
    """
    access_uri = http_publish(dataset_uri)
    if not quiet:
        click.secho("Dataset accessible at ", nl=False, fg="green")
    click.secho(access_uri)
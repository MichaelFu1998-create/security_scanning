def copy(resume, quiet, dataset_uri, dest_base_uri):
    """DEPRECATED: Copy a dataset to a different location."""
    click.secho(
        "The ``dtool copy`` command is deprecated",
        fg="red",
        err=True
    )
    click.secho(
        "Use ``dtool cp`` instead",
        fg="red",
        err=True
    )
    _copy(resume, quiet, dataset_uri, dest_base_uri)
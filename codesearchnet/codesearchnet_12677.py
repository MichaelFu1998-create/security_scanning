def cli(sample, dry_run, limit, no_limit,
        database_filename, template_filename, config_filename):
    """Command line interface."""
    # pylint: disable=too-many-arguments
    mailmerge.api.main(
        sample=sample,
        dry_run=dry_run,
        limit=limit,
        no_limit=no_limit,
        database_filename=database_filename,
        template_filename=template_filename,
        config_filename=config_filename,
    )
def check(file,  # pylint:disable=redefined-builtin
          version,
          definition):
    """Check a polyaxonfile."""
    file = file or 'polyaxonfile.yaml'
    specification = check_polyaxonfile(file).specification

    if version:
        Printer.decorate_format_value('The version is: {}',
                                      specification.version,
                                      'yellow')

    if definition:
        job_condition = (specification.is_job or
                         specification.is_build or
                         specification.is_notebook or
                         specification.is_tensorboard)
        if specification.is_experiment:
            Printer.decorate_format_value('This polyaxon specification has {}',
                                          'One experiment',
                                          'yellow')
        if job_condition:
            Printer.decorate_format_value('This {} polyaxon specification is valid',
                                          specification.kind,
                                          'yellow')
        if specification.is_group:
            experiments_def = specification.experiments_def
            click.echo(
                'This polyaxon specification has experiment group with the following definition:')
            get_group_experiments_info(**experiments_def)

    return specification
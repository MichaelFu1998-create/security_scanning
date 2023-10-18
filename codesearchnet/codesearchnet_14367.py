def update(check, enter_parameters, version):
    """
    Update package with latest template. Must be inside of the project
    folder to run.

    Using "-e" will prompt for re-entering the template parameters again
    even if the project is up to date.

    Use "-v" to update to a particular version of a template.

    Using "-c" will perform a check that the project is up to date
    with the latest version of the template (or the version specified by "-v").
    No updating will happen when using this option.
    """
    if check:
        if temple.update.up_to_date(version=version):
            print('Temple package is up to date')
        else:
            msg = (
                'This temple package is out of date with the latest template.'
                ' Update your package by running "temple update" and commiting changes.'
            )
            raise temple.exceptions.NotUpToDateWithTemplateError(msg)
    else:
        temple.update.update(new_version=version, enter_parameters=enter_parameters)
def _error_string(error, k=None):
    """String representation of SBMLError.

    Parameters
    ----------
    error : libsbml.SBMLError
    k : index of error

    Returns
    -------
    string representation of error
    """
    package = error.getPackage()
    if package == '':
        package = 'core'

    template = 'E{} ({}): {} ({}, L{}); {}; {}'
    error_str = template.format(k, error.getSeverityAsString(),
                                error.getCategoryAsString(), package,
                                error.getLine(), error.getShortMessage(),
                                error.getMessage())
    return error_str
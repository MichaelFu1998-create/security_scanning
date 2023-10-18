def read_coverage_data():
    """
    :rtype: CoverageData or None
    """
    print('Using coverage data from .coverage file')
    # noinspection PyPackageRequirements,PyUnresolvedReferences
    from coverage import Coverage
    cov = Coverage('.coverage')
    cov.load()
    return cov.get_data()
def _validate_zip(the_zip):
    """Validate zipped data package
    """
    datapackage_jsons = [f for f in the_zip.namelist() if f.endswith('datapackage.json')]
    if len(datapackage_jsons) != 1:
        msg = 'DataPackage must have only one "datapackage.json" (had {n})'
        raise exceptions.DataPackageException(msg.format(n=len(datapackage_jsons)))
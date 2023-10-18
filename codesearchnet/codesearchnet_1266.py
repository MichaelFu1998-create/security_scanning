def __getDBNameForVersion(cls, dbVersion):
    """ Generates the ClientJobs database name for the given version of the
    database

    Parameters:
    ----------------------------------------------------------------
    dbVersion:      ClientJobs database version number

    retval:         the ClientJobs database name for the given DB version
    """

    # DB Name prefix for the given version
    prefix = cls.__getDBNamePrefixForVersion(dbVersion)

    # DB Name suffix
    suffix = Configuration.get('nupic.cluster.database.nameSuffix')

    # Replace dash and dot with underscore (e.g. 'ec2-user' or ec2.user will break SQL)
    suffix = suffix.replace("-", "_")
    suffix = suffix.replace(".", "_")

    # Create the name of the database for the given DB version
    dbName = '%s_%s' % (prefix, suffix)

    return dbName
def datafile_from_hash(hash_, prefix, path):
        """Return pathlib.Path for a data-file with given hash and prefix.
        """
        pattern = '%s_%s*.h*' % (prefix, hash_)
        datafiles = list(path.glob(pattern))
        if len(datafiles) == 0:
            raise NoMatchError('No matches for "%s"' % pattern)
        if len(datafiles) > 1:
            raise MultipleMatchesError('More than 1 match for "%s"' % pattern)
        return datafiles[0]
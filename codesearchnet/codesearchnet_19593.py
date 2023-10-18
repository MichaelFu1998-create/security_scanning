def _clean_up(paths):
    """
    Clean up after ourselves, removing created files.
    @param {[String]} A list of file paths specifying the files we've created
        during run. Will all be deleted.
    @return {None}
    """
    print('Cleaning up')
    # Iterate over the given paths, unlinking them
    for path in paths:
        print('Removing %s' % path)
        os.unlink(path)
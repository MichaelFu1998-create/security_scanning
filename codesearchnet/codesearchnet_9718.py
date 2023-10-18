def create_file(fname=None, fname_tmp=None, tmpdir=None,
                save_tmpfile=False, keepext=False):
    """Context manager for making files with possibility of failure.

    If you are creating a file, it is possible that the code will fail
    and leave a corrupt intermediate file.  This is especially damaging
    if this is used as automatic input to another process.  This context
    manager helps by creating a temporary filename, your code runs and
    creates that temporary file, and then if no exceptions are raised,
    the context manager will move the temporary file to the original
    filename you intended to open.

    Parameters
    ----------
    fname : str
        Target filename, this file will be created if all goes well
    fname_tmp : str
        If given, this is used as the temporary filename.
    tmpdir : str or bool
        If given, put temporary files in this directory.  If `True`,
        then find a good tmpdir that is not on local filesystem.
    save_tmpfile : bool
        If true, the temporary file is not deleteted if an exception
        is raised.
    keepext : bool, default False
            If true, have tmpfile have same extension as final file.

    Returns (as context manager value)
    ----------------------------------
     fname_tmp: str
        Temporary filename to be used.  Same as `fname_tmp`
        if given as an argument.

    Raises
    ------
    Re-raises any except occuring during the context block.
    """
    # Do nothing if requesting sqlite memory DB.
    if fname == ':memory:':
        yield fname
        return
    if fname_tmp is None:
        # no tmpfile name given - compute some basic info
        basename = os.path.basename(fname)
        root, ext = os.path.splitext(basename)
        dir_ = this_dir = os.path.dirname(fname)
        # Remove filename extension, in case this matters for
        # automatic things itself.
        if not keepext:
            root = root + ext
            ext = ''
        if tmpdir:
            # we should use a different temporary directory
            if tmpdir is True:
                # Find a directory ourself, searching some common
                # places.
                for dir__ in possible_tmpdirs:
                    if os.access(dir__, os.F_OK):
                        dir_ = dir__
                        break
        # Make the actual tmpfile, with our chosen tmpdir, directory,
        # extension.  Set it to not delete automatically, since on
        # success we will move it to elsewhere.
        tmpfile = tempfile.NamedTemporaryFile(
            prefix='tmp-' + root + '-', suffix=ext, dir=dir_, delete=False)
        fname_tmp = tmpfile.name
    try:
        yield fname_tmp
    except Exception as e:
        if save_tmpfile:
            print("Temporary file is '%s'" % fname_tmp)
        else:
            os.unlink(fname_tmp)
        raise
    # Move the file back to the original location.
    try:
        os.rename(fname_tmp, fname)
        # We have to manually set permissions.  tempfile does not use
        # umask, for obvious reasons.
        os.chmod(fname, 0o777 & ~current_umask)
    # 'Invalid cross-device link' - you can't rename files across
    # filesystems.  So, we have to fallback to moving it.  But, we
    # want to move it using tmpfiles also, so that the final file
    # appearing is atomic.  We use... tmpfiles.
    except OSError as e:
        # New temporary file in same directory
        tmpfile2 = tempfile.NamedTemporaryFile(
            prefix='tmp-' + root + '-', suffix=ext, dir=this_dir, delete=False)
        # Copy contents over
        shutil.copy(fname_tmp, tmpfile2.name)
        # Rename new tmpfile, unlink old one on other filesystem.
        os.rename(tmpfile2.name, fname)
        os.chmod(fname, 0o666 & ~current_umask)
        os.unlink(fname_tmp)
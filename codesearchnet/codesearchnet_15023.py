def auto_detect(workdir):
    """ Return string signifying the SCM used in the given directory.

        Currently, 'git' is supported. Anything else returns 'unknown'.
    """
    # Any additions here also need a change to `SCM_PROVIDERS`!
    if os.path.isdir(os.path.join(workdir, '.git')) and os.path.isfile(os.path.join(workdir, '.git', 'HEAD')):
        return 'git'

    return 'unknown'
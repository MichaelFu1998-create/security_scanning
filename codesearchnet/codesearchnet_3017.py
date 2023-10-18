def Split(self):
    """Splits the file into the directory, basename, and extension.

    For 'chrome/browser/browser.cc', Split() would
    return ('chrome/browser', 'browser', '.cc')

    Returns:
      A tuple of (directory, basename, extension).
    """

    googlename = self.RepositoryName()
    project, rest = os.path.split(googlename)
    return (project,) + os.path.splitext(rest)
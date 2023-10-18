def locate(pattern, root=os.curdir):
    """Locate all files matching supplied filename pattern recursively."""
    for path, dummy, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)
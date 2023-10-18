def create_tarfile(files, project_name):
    """Create a tar file based on the list of files passed"""
    fd, filename = tempfile.mkstemp(prefix="polyaxon_{}".format(project_name), suffix='.tar.gz')
    with tarfile.open(filename, "w:gz") as tar:
        for f in files:
            tar.add(f)

    yield filename

    # clear
    os.close(fd)
    os.remove(filename)
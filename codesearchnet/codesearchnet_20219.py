def datapackage_exists(repo):
    """
    Check if the datapackage exists...
    """
    datapath = os.path.join(repo.rootdir, "datapackage.json")
    return os.path.exists(datapath)
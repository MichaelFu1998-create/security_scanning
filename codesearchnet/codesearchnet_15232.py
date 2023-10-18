def upload_backend(index='dev', user=None):
    """
    Build the backend and upload it to the remote server at the given index
    """
    get_vars()
    use_devpi(index=index)
    with fab.lcd('../application'):
        fab.local('make upload')
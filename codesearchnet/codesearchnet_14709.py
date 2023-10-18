def operation_list(uploader):
    """List file on target"""
    files = uploader.file_list()
    for f in files:
        log.info("{file:30s} {size}".format(file=f[0], size=f[1]))
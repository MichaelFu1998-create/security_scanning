def operation_download(uploader, sources):
    """The download operation"""
    sources, destinations = destination_from_source(sources, False)
    print('sources', sources)
    print('destinations', destinations)
    if len(destinations) == len(sources):
        if uploader.prepare():
            for filename, dst in zip(sources, destinations):
                uploader.read_file(filename, dst)
    else:
        raise Exception('You must specify a destination filename for each file you want to download.')
    log.info('All done!')
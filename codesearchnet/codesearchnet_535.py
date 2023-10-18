def maybe_download_and_extract(filename, working_directory, url_source, extract=False, expected_bytes=None):
    """Checks if file exists in working_directory otherwise tries to dowload the file,
    and optionally also tries to extract the file if format is ".zip" or ".tar"

    Parameters
    -----------
    filename : str
        The name of the (to be) dowloaded file.
    working_directory : str
        A folder path to search for the file in and dowload the file to
    url : str
        The URL to download the file from
    extract : boolean
        If True, tries to uncompress the dowloaded file is ".tar.gz/.tar.bz2" or ".zip" file, default is False.
    expected_bytes : int or None
        If set tries to verify that the downloaded file is of the specified size, otherwise raises an Exception, defaults is None which corresponds to no check being performed.

    Returns
    ----------
    str
        File path of the dowloaded (uncompressed) file.

    Examples
    --------
    >>> down_file = tl.files.maybe_download_and_extract(filename='train-images-idx3-ubyte.gz',
    ...                                            working_directory='data/',
    ...                                            url_source='http://yann.lecun.com/exdb/mnist/')
    >>> tl.files.maybe_download_and_extract(filename='ADEChallengeData2016.zip',
    ...                                             working_directory='data/',
    ...                                             url_source='http://sceneparsing.csail.mit.edu/data/',
    ...                                             extract=True)

    """

    # We first define a download function, supporting both Python 2 and 3.
    def _download(filename, working_directory, url_source):

        progress_bar = progressbar.ProgressBar()

        def _dlProgress(count, blockSize, totalSize, pbar=progress_bar):
            if (totalSize != 0):

                if not pbar.max_value:
                    totalBlocks = math.ceil(float(totalSize) / float(blockSize))
                    pbar.max_value = int(totalBlocks)

                pbar.update(count, force=True)

        filepath = os.path.join(working_directory, filename)

        logging.info('Downloading %s...\n' % filename)

        urlretrieve(url_source + filename, filepath, reporthook=_dlProgress)

    exists_or_mkdir(working_directory, verbose=False)
    filepath = os.path.join(working_directory, filename)

    if not os.path.exists(filepath):

        _download(filename, working_directory, url_source)
        statinfo = os.stat(filepath)
        logging.info('Succesfully downloaded %s %s bytes.' % (filename, statinfo.st_size))  # , 'bytes.')
        if (not (expected_bytes is None) and (expected_bytes != statinfo.st_size)):
            raise Exception('Failed to verify ' + filename + '. Can you get to it with a browser?')
        if (extract):
            if tarfile.is_tarfile(filepath):
                logging.info('Trying to extract tar file')
                tarfile.open(filepath, 'r').extractall(working_directory)
                logging.info('... Success!')
            elif zipfile.is_zipfile(filepath):
                logging.info('Trying to extract zip file')
                with zipfile.ZipFile(filepath) as zf:
                    zf.extractall(working_directory)
                logging.info('... Success!')
            else:
                logging.info("Unknown compression_format only .tar.gz/.tar.bz2/.tar and .zip supported")
    return filepath
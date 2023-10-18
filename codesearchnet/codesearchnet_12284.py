def s3_get_url(url,
               altexts=None,
               client=None,
               raiseonfail=False):
    """This gets a file from an S3 bucket based on its s3:// URL.

    Parameters
    ----------

    url : str
        S3 URL to download. This should begin with 's3://'.

    altexts : None or list of str
        If not None, this is a list of alternate extensions to try for the file
        other than the one provided in `filename`. For example, to get anything
        that's an .sqlite where .sqlite.gz is expected, use altexts=[''] to
        strip the .gz.

    client : boto3.Client or None
        If None, this function will instantiate a new `boto3.Client` object to
        use in its operations. Alternatively, pass in an existing `boto3.Client`
        instance to re-use it here.

    raiseonfail : bool
        If True, will re-raise whatever Exception caused the operation to fail
        and break out immediately.

    Returns
    -------

    str
        Path to the downloaded filename or None if the download was
        unsuccessful. The file will be downloaded into the current working
        directory and will have a filename == basename of the file on S3.

    """

    bucket_item = url.replace('s3://','')
    bucket_item = bucket_item.split('/')
    bucket = bucket_item[0]
    filekey = '/'.join(bucket_item[1:])

    return s3_get_file(bucket,
                       filekey,
                       bucket_item[-1],
                       altexts=altexts,
                       client=client,
                       raiseonfail=raiseonfail)
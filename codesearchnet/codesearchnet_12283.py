def s3_get_file(bucket,
                filename,
                local_file,
                altexts=None,
                client=None,
                raiseonfail=False):

    """This gets a file from an S3 bucket.

    Parameters
    ----------

    bucket : str
        The AWS S3 bucket name.

    filename : str
        The full filename of the file to get from the bucket

    local_file : str
        Path to where the downloaded file will be stored.

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
        unsuccessful.

    """

    if not client:
        client = boto3.client('s3')

    try:

        client.download_file(bucket, filename, local_file)
        return local_file

    except Exception as e:

        if altexts is not None:

            for alt_extension in altexts:

                split_ext = os.path.splitext(filename)
                check_file = split_ext[0] + alt_extension
                try:
                    client.download_file(
                        bucket,
                        check_file,
                        local_file.replace(split_ext[-1],
                                           alt_extension)
                    )
                    return local_file.replace(split_ext[-1],
                                              alt_extension)
                except Exception as e:
                    pass

        else:

            LOGEXCEPTION('could not download s3://%s/%s' % (bucket, filename))

            if raiseonfail:
                raise

            return None
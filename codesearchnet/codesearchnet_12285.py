def s3_put_file(local_file, bucket, client=None, raiseonfail=False):
    """This uploads a file to S3.

    Parameters
    ----------

    local_file : str
        Path to the file to upload to S3.

    bucket : str
        The AWS S3 bucket to upload the file to.

    client : boto3.Client or None
        If None, this function will instantiate a new `boto3.Client` object to
        use in its operations. Alternatively, pass in an existing `boto3.Client`
        instance to re-use it here.

    raiseonfail : bool
        If True, will re-raise whatever Exception caused the operation to fail
        and break out immediately.

    Returns
    -------

    str or None
        If the file upload is successful, returns the s3:// URL of the uploaded
        file. If it failed, will return None.

    """

    if not client:
        client = boto3.client('s3')

    try:
        client.upload_file(local_file, bucket, os.path.basename(local_file))
        return 's3://%s/%s' % (bucket, os.path.basename(local_file))
    except Exception as e:
        LOGEXCEPTION('could not upload %s to bucket: %s' % (local_file,
                                                            bucket))

        if raiseonfail:
            raise

        return None
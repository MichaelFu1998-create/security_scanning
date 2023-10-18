def s3_delete_file(bucket, filename, client=None, raiseonfail=False):
    """This deletes a file from S3.

    Parameters
    ----------

    bucket : str
        The AWS S3 bucket to delete the file from.

    filename : str
        The full file name of the file to delete, including any prefixes.

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
        If the file was successfully deleted, will return the delete-marker
        (https://docs.aws.amazon.com/AmazonS3/latest/dev/DeleteMarker.html). If
        it wasn't, returns None

    """

    if not client:
        client = boto3.client('s3')

    try:
        resp = client.delete_object(Bucket=bucket, Key=filename)
        if not resp:
            LOGERROR('could not delete file %s from bucket %s' % (filename,
                                                                  bucket))
        else:
            return resp['DeleteMarker']
    except Exception as e:
        LOGEXCEPTION('could not delete file %s from bucket %s' % (filename,
                                                                  bucket))
        if raiseonfail:
            raise

        return None
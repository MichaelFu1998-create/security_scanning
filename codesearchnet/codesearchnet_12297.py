def gcs_get_url(url,
                altexts=None,
                client=None,
                service_account_json=None,
                raiseonfail=False):
    """This gets a single file from a Google Cloud Storage bucket.

    This uses the gs:// URL instead of a bucket name and key.

    Parameters
    ----------

    url : str
        GCS URL to download. This should begin with 'gs://'.

    altexts : None or list of str
        If not None, this is a list of alternate extensions to try for the file
        other than the one provided in `filename`. For example, to get anything
        that's an .sqlite where .sqlite.gz is expected, use altexts=[''] to
        strip the .gz.

    client : google.cloud.storage.Client instance
        The instance of the Client to use to perform the download operation. If
        this is None, a new Client will be used. If this is None and
        `service_account_json` points to a downloaded JSON file with GCS
        credentials, a new Client with the provided credentials will be used. If
        this is not None, the existing Client instance will be used.

    service_account_json : str
        Path to a downloaded GCS credentials JSON file.

    raiseonfail : bool
        If True, will re-raise whatever Exception caused the operation to fail
        and break out immediately.

    Returns
    -------

    str
        Path to the downloaded filename or None if the download was
        unsuccessful.

    """
    bucket_item = url.replace('gs://','')
    bucket_item = bucket_item.split('/')
    bucket = bucket_item[0]
    filekey = '/'.join(bucket_item[1:])

    return gcs_get_file(bucket,
                        filekey,
                        bucket_item[-1],
                        altexts=altexts,
                        client=client,
                        service_account_json=service_account_json,
                        raiseonfail=raiseonfail)
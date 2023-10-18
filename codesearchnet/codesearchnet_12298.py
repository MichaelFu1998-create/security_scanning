def gcs_put_file(local_file,
                 bucketname,
                 service_account_json=None,
                 client=None,
                 raiseonfail=False):
    """This puts a single file into a Google Cloud Storage bucket.

    Parameters
    ----------

    local_file : str
        Path to the file to upload to GCS.

    bucket : str
        The GCS bucket to upload the file to.

    service_account_json : str
        Path to a downloaded GCS credentials JSON file.

    client : google.cloud.storage.Client instance
        The instance of the Client to use to perform the download operation. If
        this is None, a new Client will be used. If this is None and
        `service_account_json` points to a downloaded JSON file with GCS
        credentials, a new Client with the provided credentials will be used. If
        this is not None, the existing Client instance will be used.

    raiseonfail : bool
        If True, will re-raise whatever Exception caused the operation to fail
        and break out immediately.

    Returns
    -------

    str or None
        If the file upload is successful, returns the gs:// URL of the uploaded
        file. If it failed, will return None.

    """

    if not client:

        if (service_account_json is not None and
            os.path.exists(service_account_json)):
            client = storage.Client.from_service_account_json(
                service_account_json
            )
        else:
            client = storage.Client()

    try:

        bucket = client.get_bucket(bucketname)
        remote_blob = bucket.blob(local_file)
        remote_blob.upload_from_filename(local_file)
        return 'gs://%s/%s' % (bucketname, local_file.lstrip('/'))

    except Exception as e:

        LOGEXCEPTION('could not upload %s to bucket %s' % (local_file,
                                                           bucket))

        if raiseonfail:
            raise

        return None
def gcs_get_file(bucketname,
                 filename,
                 local_file,
                 altexts=None,
                 client=None,
                 service_account_json=None,
                 raiseonfail=False):
    """This gets a single file from a Google Cloud Storage bucket.

    Parameters
    ----------

    bucketname : str
        The name of the GCS bucket to download the file from.

    filename : str
        The full name of the file to download, including all prefixes.

    local_file : str
        Path to where the downloaded file will be stored.

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
        blob = bucket.get_blob(filename)
        blob.download_to_filename(local_file)
        return local_file

    except Exception as e:

        for alt_extension in altexts:

            split_ext = os.path.splitext(filename)
            check_file = split_ext[0] + alt_extension
            try:
                bucket = client.get_bucket(bucket)
                blob = bucket.get_blob(check_file)
                blob.download_to_filename(
                    local_file.replace(split_ext[-1],
                                       alt_extension)
                )
                return local_file.replace(split_ext[-1],
                                          alt_extension)
            except Exception as e:
                pass

    else:

        LOGEXCEPTION('could not download gs://%s/%s' % (bucket, filename))

        if raiseonfail:
            raise

        return None
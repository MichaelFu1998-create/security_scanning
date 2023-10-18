def _prefix_exists_in_gcs(gcs_prefix, credentials=None):
  """Check whether there is a GCS object whose name starts with the prefix.

  Since GCS doesn't actually have folders, this is how we check instead.

  Args:
    gcs_prefix: The path; should start with 'gs://'.
    credentials: Optional credential to be used to load the file from gcs.

  Returns:
    True if the prefix matches at least one object in GCS.

  Raises:
    errors.HttpError: if it can't talk to the server
  """
  gcs_service = _get_storage_service(credentials)

  bucket_name, prefix = gcs_prefix[len('gs://'):].split('/', 1)
  # documentation in
  # https://cloud.google.com/storage/docs/json_api/v1/objects/list
  request = gcs_service.objects().list(
      bucket=bucket_name, prefix=prefix, maxResults=1)
  response = request.execute()
  return response.get('items', None)
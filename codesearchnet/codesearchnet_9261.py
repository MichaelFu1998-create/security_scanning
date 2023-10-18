def _file_exists_in_gcs(gcs_file_path, credentials=None):
  """Check whether the file exists, in GCS.

  Args:
    gcs_file_path: The target file path; should have the 'gs://' prefix.
    credentials: Optional credential to be used to load the file from gcs.

  Returns:
    True if the file's there.
  """
  gcs_service = _get_storage_service(credentials)

  bucket_name, object_name = gcs_file_path[len('gs://'):].split('/', 1)
  request = gcs_service.objects().get(
      bucket=bucket_name, object=object_name, projection='noAcl')
  try:
    request.execute()
    return True
  except errors.HttpError:
    return False
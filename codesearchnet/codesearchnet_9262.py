def file_exists(file_path, credentials=None):
  """Check whether the file exists, on local disk or GCS.

  Args:
    file_path: The target file path; should have the 'gs://' prefix if in gcs.
    credentials: Optional credential to be used to load the file from gcs.

  Returns:
    True if the file's there.
  """
  if file_path.startswith('gs://'):
    return _file_exists_in_gcs(file_path, credentials)
  else:
    return os.path.isfile(file_path)
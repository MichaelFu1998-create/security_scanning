def load_file(file_path, credentials=None):
  """Load a file from either local or gcs.

  Args:
    file_path: The target file path, which should have the prefix 'gs://' if
               to be loaded from gcs.
    credentials: Optional credential to be used to load the file from gcs.

  Returns:
    A python File object if loading file from local or a StringIO object if
    loading from gcs.
  """
  if file_path.startswith('gs://'):
    return _load_file_from_gcs(file_path, credentials)
  else:
    return open(file_path, 'r')
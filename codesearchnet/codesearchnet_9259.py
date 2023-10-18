def _load_file_from_gcs(gcs_file_path, credentials=None):
  """Load context from a text file in gcs.

  Args:
    gcs_file_path: The target file path; should have the 'gs://' prefix.
    credentials: Optional credential to be used to load the file from gcs.

  Returns:
    The content of the text file as a string.
  """
  gcs_service = _get_storage_service(credentials)

  bucket_name, object_name = gcs_file_path[len('gs://'):].split('/', 1)
  request = gcs_service.objects().get_media(
      bucket=bucket_name, object=object_name)

  file_handle = io.BytesIO()
  downloader = MediaIoBaseDownload(file_handle, request, chunksize=1024 * 1024)
  done = False
  while not done:
    _, done = _downloader_next_chunk(downloader)
  filevalue = file_handle.getvalue()
  if not isinstance(filevalue, six.string_types):
    filevalue = filevalue.decode()
  return six.StringIO(filevalue)
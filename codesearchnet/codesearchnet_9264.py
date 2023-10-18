def simple_pattern_exists_in_gcs(file_pattern, credentials=None):
  """True iff an object exists matching the input GCS pattern.

  The GCS pattern must be a full object reference or a "simple pattern" that
  conforms to the dsub input and output parameter restrictions:

    * No support for **, ? wildcards or [] character ranges
    * Wildcards may only appear in the file name

  Args:
    file_pattern: eg. 'gs://foo/ba*'
    credentials: Optional credential to be used to load the file from gcs.

  Raises:
    ValueError: if file_pattern breaks the rules.

  Returns:
    True iff a file exists that matches that pattern.
  """
  if '*' not in file_pattern:
    return _file_exists_in_gcs(file_pattern, credentials)
  if not file_pattern.startswith('gs://'):
    raise ValueError('file name must start with gs://')
  gcs_service = _get_storage_service(credentials)
  bucket_name, prefix = file_pattern[len('gs://'):].split('/', 1)
  if '*' in bucket_name:
    raise ValueError('Wildcards may not appear in the bucket name')
  # There is a '*' in prefix because we checked there's one in file_pattern
  # and there isn't one in bucket_name. Hence it must be in prefix.
  assert '*' in prefix
  prefix_no_wildcard = prefix[:prefix.index('*')]
  request = gcs_service.objects().list(
      bucket=bucket_name, prefix=prefix_no_wildcard)
  response = request.execute()
  if 'items' not in response:
    return False
  items_list = [i['name'] for i in response['items']]
  return any(fnmatch.fnmatch(i, prefix) for i in items_list)
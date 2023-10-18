def validate_bucket_name(bucket):
  """Validate that the name is a valid GCS bucket."""
  if not bucket.startswith('gs://'):
    raise ValueError(
        'Invalid bucket path "%s". Must start with "gs://".' % bucket)
  bucket_name = bucket[len('gs://'):]
  if not re.search(r'^\w[\w_\.-]{1,61}\w$', bucket_name):
    raise ValueError('Invalid bucket name: %s' % bucket)
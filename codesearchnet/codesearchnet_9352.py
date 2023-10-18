def parse_file_provider(uri):
    """Find the file provider for a URI."""
    providers = {'gs': job_model.P_GCS, 'file': job_model.P_LOCAL}
    # URI scheme detector uses a range up to 30 since none of the IANA
    # registered schemes are longer than this.
    provider_found = re.match(r'^([A-Za-z][A-Za-z0-9+.-]{0,29})://', uri)
    if provider_found:
      prefix = provider_found.group(1).lower()
    else:
      # If no provider is specified in the URI, assume that the local
      # filesystem is being used. Availability and validity of the local
      # file/directory will be checked later.
      prefix = 'file'
    if prefix in providers:
      return providers[prefix]
    else:
      raise ValueError('File prefix not supported: %s://' % prefix)
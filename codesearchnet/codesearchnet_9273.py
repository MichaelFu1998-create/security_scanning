def list(cls, service, ops_filter, page_size=0):
    """Gets the list of operations for the specified filter.

    Args:
      service: Google Genomics API service object
      ops_filter: string filter of operations to return
      page_size: the number of operations to requested on each list operation to
        the pipelines API (if 0 or None, the API default is used)

    Yields:
      Operations matching the filter criteria.
    """

    page_token = None
    more_operations = True
    documented_default_page_size = 256
    documented_max_page_size = 2048

    if not page_size:
      page_size = documented_default_page_size
    page_size = min(page_size, documented_max_page_size)

    while more_operations:
      api = service.operations().list(
          name='operations',
          filter=ops_filter,
          pageToken=page_token,
          pageSize=page_size)
      response = google_base.Api.execute(api)

      ops = response.get('operations', [])
      for op in ops:
        if cls.is_dsub_operation(op):
          yield GoogleOperation(op)

      page_token = response.get('nextPageToken')
      more_operations = bool(page_token)
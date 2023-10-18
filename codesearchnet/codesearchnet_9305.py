def _operations_list(self, ops_filter, max_tasks, page_size, page_token):
    """Gets the list of operations for the specified filter.

    Args:
      ops_filter: string filter of operations to return
      max_tasks: the maximum number of job tasks to return or 0 for no limit.
      page_size: the number of operations to requested on each list operation to
        the pipelines API (if 0 or None, the API default is used)
      page_token: page token returned by a previous _operations_list call.

    Returns:
      Operations matching the filter criteria.
    """

    # We are not using the documented default page size of 256,
    # nor allowing for the maximum page size of 2048 as larger page sizes
    # currently cause the operations.list() API to return an error:
    # HttpError 429 ... Resource has been exhausted (e.g. check quota).
    max_page_size = 128

    # Set the page size to the smallest (non-zero) size we can
    page_size = min(sz for sz in [page_size, max_page_size, max_tasks] if sz)

    # Execute operations.list() and return all of the dsub operations
    api = self._service.projects().operations().list(
        name='projects/{}/operations'.format(self._project),
        filter=ops_filter,
        pageToken=page_token,
        pageSize=page_size)
    response = google_base.Api.execute(api)

    return [
        GoogleOperation(op)
        for op in response.get('operations', [])
        if google_v2_operations.is_dsub_operation(op)
    ], response.get('nextPageToken')
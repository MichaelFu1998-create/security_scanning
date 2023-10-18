def _operation_status(self):
    """Returns the status of this operation.

    Raises:
      ValueError: if the operation status cannot be determined.

    Returns:
      A printable status string (RUNNING, SUCCESS, CANCELED or FAILURE).
    """
    if not google_v2_operations.is_done(self._op):
      return 'RUNNING'
    if google_v2_operations.is_success(self._op):
      return 'SUCCESS'
    if google_v2_operations.is_canceled(self._op):
      return 'CANCELED'
    if google_v2_operations.is_failed(self._op):
      return 'FAILURE'

    raise ValueError('Status for operation {} could not be determined'.format(
        self._op['name']))
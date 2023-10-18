def _cancel_batch(batch_fn, cancel_fn, ops):
  """Cancel a batch of operations.

  Args:
    batch_fn: API-specific batch function.
    cancel_fn: API-specific cancel function.
    ops: A list of operations to cancel.

  Returns:
    A list of operations canceled and a list of error messages.
  """

  # We define an inline callback which will populate a list of
  # successfully canceled operations as well as a list of operations
  # which were not successfully canceled.

  canceled = []
  failed = []

  def handle_cancel_response(request_id, response, exception):
    """Callback for the cancel response."""
    del response  # unused

    if exception:
      # We don't generally expect any failures here, except possibly trying
      # to cancel an operation that is already canceled or finished.
      #
      # If the operation is already finished, provide a clearer message than
      # "error 400: Bad Request".

      msg = 'error %s: %s' % (exception.resp.status, exception.resp.reason)
      if exception.resp.status == FAILED_PRECONDITION_CODE:
        detail = json.loads(exception.content)
        status = detail.get('error', {}).get('status')
        if status == FAILED_PRECONDITION_STATUS:
          msg = 'Not running'

      failed.append({'name': request_id, 'msg': msg})
    else:
      canceled.append({'name': request_id})

    return

  # Set up the batch object
  batch = batch_fn(callback=handle_cancel_response)

  # The callback gets a "request_id" which is the operation name.
  # Build a dict such that after the callback, we can lookup the operation
  # objects by name
  ops_by_name = {}
  for op in ops:
    op_name = op.get_field('internal-id')
    ops_by_name[op_name] = op
    batch.add(cancel_fn(name=op_name, body={}), request_id=op_name)

  # Cancel the operations
  batch.execute()

  # Iterate through the canceled and failed lists to build our return lists
  canceled_ops = [ops_by_name[op['name']] for op in canceled]
  error_messages = []
  for fail in failed:
    op = ops_by_name[fail['name']]
    error_messages.append("Error canceling '%s': %s" %
                          (get_operation_full_job_id(op), fail['msg']))

  return canceled_ops, error_messages
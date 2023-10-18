def cancel(batch_fn, cancel_fn, ops):
  """Cancel operations.

  Args:
    batch_fn: API-specific batch function.
    cancel_fn: API-specific cancel function.
    ops: A list of operations to cancel.

  Returns:
    A list of operations canceled and a list of error messages.
  """

  # Canceling many operations one-by-one can be slow.
  # The Pipelines API doesn't directly support a list of operations to cancel,
  # but the requests can be performed in batch.

  canceled_ops = []
  error_messages = []

  max_batch = 256
  total_ops = len(ops)
  for first_op in range(0, total_ops, max_batch):
    batch_canceled, batch_messages = _cancel_batch(
        batch_fn, cancel_fn, ops[first_op:first_op + max_batch])
    canceled_ops.extend(batch_canceled)
    error_messages.extend(batch_messages)

  return canceled_ops, error_messages
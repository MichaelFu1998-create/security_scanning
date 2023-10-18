def sqs_delete_item(queue_url,
                    receipt_handle,
                    client=None,
                    raiseonfail=False):
    """This deletes a message from the queue, effectively acknowledging its
    receipt.

    Call this only when all messages retrieved from the queue have been
    processed, since this will prevent redelivery of these messages to other
    queue workers pulling fromn the same queue channel.

    Parameters
    ----------

    queue_url : str
        The SQS URL of the queue where we got the messages from. This should be
        the same queue used to retrieve the messages in `sqs_get_item`.

    receipt_handle : str
        The receipt handle of the queue message that we're responding to, and
        will acknowledge receipt of. This will be present in each message
        retrieved using `sqs_get_item`.

    client : boto3.Client or None
        If None, this function will instantiate a new `boto3.Client` object to
        use in its operations. Alternatively, pass in an existing `boto3.Client`
        instance to re-use it here.

    raiseonfail : bool
        If True, will re-raise whatever Exception caused the operation to fail
        and break out immediately.

    Returns
    -------

    Nothing.

    """

    if not client:
        client = boto3.client('sqs')

    try:

        client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )

    except Exception as e:

        LOGEXCEPTION(
            'could not delete message with receipt handle: '
            '%s from queue: %s' % (receipt_handle, queue_url)
        )

        if raiseonfail:
            raise
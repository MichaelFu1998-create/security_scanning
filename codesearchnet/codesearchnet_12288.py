def sqs_delete_queue(queue_url, client=None):
    """This deletes an SQS queue given its URL

    Parameters
    ----------

    queue_url : str
        The SQS URL of the queue to delete.

    client : boto3.Client or None
        If None, this function will instantiate a new `boto3.Client` object to
        use in its operations. Alternatively, pass in an existing `boto3.Client`
        instance to re-use it here.

    Returns
    -------

    bool
        True if the queue was deleted successfully. False otherwise.

    """

    if not client:
        client = boto3.client('sqs')

    try:

        client.delete_queue(QueueUrl=queue_url)
        return True

    except Exception as e:
        LOGEXCEPTION('could not delete the specified queue: %s'
                     % (queue_url,))
        return False
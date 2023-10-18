def sqs_put_item(queue_url,
                 item,
                 delay_seconds=0,
                 client=None,
                 raiseonfail=False):
    """This pushes a dict serialized to JSON to the specified SQS queue.

    Parameters
    ----------

    queue_url : str
        The SQS URL of the queue to push the object to.

    item : dict
        The dict passed in here will be serialized to JSON.

    delay_seconds : int
        The amount of time in seconds the pushed item will be held before going
        'live' and being visible to all queue consumers.

    client : boto3.Client or None
        If None, this function will instantiate a new `boto3.Client` object to
        use in its operations. Alternatively, pass in an existing `boto3.Client`
        instance to re-use it here.

    raiseonfail : bool
        If True, will re-raise whatever Exception caused the operation to fail
        and break out immediately.

    Returns
    -------

    boto3.Response or None
        If the item was successfully put on the queue, will return the response
        from the service. If it wasn't, will return None.

    """

    if not client:
        client = boto3.client('sqs')

    try:

        json_msg = json.dumps(item)

        resp = client.send_message(
            QueueUrl=queue_url,
            MessageBody=json_msg,
            DelaySeconds=delay_seconds,
        )
        if not resp:
            LOGERROR('could not send item to queue: %s' % queue_url)
            return None
        else:
            return resp

    except Exception as e:

        LOGEXCEPTION('could not send item to queue: %s' % queue_url)

        if raiseonfail:
            raise

        return None
def sqs_get_item(queue_url,
                 max_items=1,
                 wait_time_seconds=5,
                 client=None,
                 raiseonfail=False):
    """This gets a single item from the SQS queue.

    The `queue_url` is composed of some internal SQS junk plus a
    `queue_name`. For our purposes (`lcproc_aws.py`), the queue name will be
    something like::

        lcproc_queue_<action>

    where action is one of::

        runcp
        runpf

    The item is always a JSON object::

        {'target': S3 bucket address of the file to process,
         'action': the action to perform on the file ('runpf', 'runcp', etc.)
         'args': the action's args as a tuple (not including filename, which is
                 generated randomly as a temporary local file),
         'kwargs': the action's kwargs as a dict,
         'outbucket: S3 bucket to write the result to,
         'outqueue': SQS queue to write the processed item's info to (optional)}

    The action MUST match the <action> in the queue name for this item to be
    processed.

    Parameters
    ----------

    queue_url : str
        The SQS URL of the queue to get messages from.

    max_items : int
        The number of items to pull from the queue in this request.

    wait_time_seconds : int
        This specifies how long the function should block until a message is
        received on the queue. If the timeout expires, an empty list will be
        returned. If the timeout doesn't expire, the function will return a list
        of items received (up to `max_items`).

    client : boto3.Client or None
        If None, this function will instantiate a new `boto3.Client` object to
        use in its operations. Alternatively, pass in an existing `boto3.Client`
        instance to re-use it here.

    raiseonfail : bool
        If True, will re-raise whatever Exception caused the operation to fail
        and break out immediately.

    Returns
    -------

    list of dicts or None
        For each item pulled from the queue in this request (up to `max_items`),
        a dict will be deserialized from the retrieved JSON, containing the
        message items and various metadata. The most important item of the
        metadata is the `receipt_handle`, which can be used to acknowledge
        receipt of all items in this request (see `sqs_delete_item` below).

        If the queue pull fails outright, returns None. If no messages are
        available for this queue pull, returns an empty list.

    """

    if not client:
        client = boto3.client('sqs')

    try:

        resp = client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=max_items,
            WaitTimeSeconds=wait_time_seconds
        )

        if not resp:
            LOGERROR('could not receive messages from queue: %s' %
                     queue_url)

        else:

            messages = []

            for msg in resp.get('Messages',[]):

                try:
                    messages.append({
                        'id':msg['MessageId'],
                        'receipt_handle':msg['ReceiptHandle'],
                        'md5':msg['MD5OfBody'],
                        'attributes':msg['Attributes'],
                        'item':json.loads(msg['Body']),
                    })
                except Exception as e:
                    LOGEXCEPTION(
                        'could not deserialize message ID: %s, body: %s' %
                        (msg['MessageId'], msg['Body'])
                    )
                    continue

            return messages

    except Exception as e:
        LOGEXCEPTION('could not get items from queue: %s' % queue_url)

        if raiseonfail:
            raise

        return None
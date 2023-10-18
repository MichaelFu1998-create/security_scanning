def sqs_create_queue(queue_name, options=None, client=None):
    """
    This creates an SQS queue.

    Parameters
    ----------

    queue_name : str
        The name of the queue to create.

    options : dict or None
        A dict of options indicate extra attributes the queue should have.
        See the SQS docs for details. If None, no custom attributes will be
        attached to the queue.

    client : boto3.Client or None
        If None, this function will instantiate a new `boto3.Client` object to
        use in its operations. Alternatively, pass in an existing `boto3.Client`
        instance to re-use it here.

    Returns
    -------

    dict
        This returns a dict of the form::

            {'url': SQS URL of the queue,
             'name': name of the queue}

    """

    if not client:
        client = boto3.client('sqs')

    try:

        if isinstance(options, dict):
            resp = client.create_queue(QueueName=queue_name, Attributes=options)
        else:
            resp = client.create_queue(QueueName=queue_name)

        if resp is not None:
            return {'url':resp['QueueUrl'],
                    'name':queue_name}
        else:
            LOGERROR('could not create the specified queue: %s with options: %s'
                     % (queue_name, options))
            return None

    except Exception as e:
        LOGEXCEPTION('could not create the specified queue: %s with options: %s'
                     % (queue_name, options))
        return None
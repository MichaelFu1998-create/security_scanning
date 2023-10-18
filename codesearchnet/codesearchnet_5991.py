def get_queue(queue, flags=FLAGS.ALL, **conn):
    """
    Orchestrates all the calls required to fully fetch details about an SQS Queue:
    
    {
        "Arn": ...,
        "Region": ...,
        "Name": ...,
        "Url": ...,
        "Attributes": ...,
        "Tags": ...,
        "DeadLetterSourceQueues": ...,
        "_version": 1
    }

    :param queue: Either the queue name OR the queue url
    :param flags: By default, set to ALL fields.
    :param conn: dict containing enough information to make a connection to the desired account. Must at least have
                 'assume_role' key.
    :return: dict containing a fully built out SQS queue.
    """
    # Check if this is a Queue URL or a queue name:
    if queue.startswith("https://") or queue.startswith("http://"):
        queue_name = queue
    else:
        queue_name = get_queue_url(QueueName=queue, **conn)

    sqs_queue = {"QueueUrl": queue_name}

    return registry.build_out(flags, sqs_queue, **conn)
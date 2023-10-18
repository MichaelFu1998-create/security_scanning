def sender(address, use_queue=True, **kwds):
    """
    :param str address: a pair (ip_address, port) to pass to socket.connect
    :param bool use_queue: if True, run the connection in a different thread
        with a queue
    """
    return QueuedSender(address, **kwds) if use_queue else Sender(address)
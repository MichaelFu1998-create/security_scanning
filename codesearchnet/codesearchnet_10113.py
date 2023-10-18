def _read_remaining(socket):
    """
    Reads everything available from the socket - used for debugging when there
    is a protocol error

    :param socket:
        The socket to read from

    :return:
        A byte string of the remaining data
    """

    output = b''
    old_timeout = socket.gettimeout()
    try:
        socket.settimeout(0.0)
        output += socket.recv(8192)
    except (socket_.error):
        pass
    finally:
        socket.settimeout(old_timeout)
    return output
def create_listening_socket(host, port, handler):
    """
    Create socket and set listening options
    :param host:
    :param port:
    :param handler:
    :return:
    """
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((host, port))
    sock.listen(1)

    GObject.io_add_watch(sock, GObject.IO_IN, handler)
    return sock
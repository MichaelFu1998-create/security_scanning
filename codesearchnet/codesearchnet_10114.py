def _write_callback(connection_id, data_buffer, data_length_pointer):
    """
    Callback called by Secure Transport to actually write to the socket

    :param connection_id:
        An integer identifing the connection

    :param data_buffer:
        A char pointer FFI type containing the data to write

    :param data_length_pointer:
        A size_t pointer FFI type of the amount of data to write. Will be
        overwritten with the amount of data actually written on return.

    :return:
        An integer status code of the result - 0 for success
    """

    try:
        self = _connection_refs.get(connection_id)
        if not self:
            socket = _socket_refs.get(connection_id)
        else:
            socket = self._socket

        if not self and not socket:
            return 0

        data_length = deref(data_length_pointer)
        data = bytes_from_buffer(data_buffer, data_length)

        if self and not self._done_handshake:
            self._client_hello += data

        error = None
        try:
            sent = socket.send(data)
        except (socket_.error) as e:
            error = e.errno

        if error is not None and error != errno.EAGAIN:
            if error == errno.ECONNRESET or error == errno.EPIPE:
                return SecurityConst.errSSLClosedNoNotify
            return SecurityConst.errSSLClosedAbort

        if sent != data_length:
            pointer_set(data_length_pointer, sent)
            return SecurityConst.errSSLWouldBlock

        return 0
    except (KeyboardInterrupt) as e:
        self._exception = e
        return SecurityConst.errSSLPeerUserCancelled
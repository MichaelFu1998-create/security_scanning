def _read_callback(connection_id, data_buffer, data_length_pointer):
    """
    Callback called by Secure Transport to actually read the socket

    :param connection_id:
        An integer identifing the connection

    :param data_buffer:
        A char pointer FFI type to write the data to

    :param data_length_pointer:
        A size_t pointer FFI type of the amount of data to read. Will be
        overwritten with the amount of data read on return.

    :return:
        An integer status code of the result - 0 for success
    """

    self = None
    try:
        self = _connection_refs.get(connection_id)
        if not self:
            socket = _socket_refs.get(connection_id)
        else:
            socket = self._socket

        if not self and not socket:
            return 0

        bytes_requested = deref(data_length_pointer)

        timeout = socket.gettimeout()
        error = None
        data = b''
        try:
            while len(data) < bytes_requested:
                # Python 2 on Travis CI seems to have issues with blocking on
                # recv() for longer than the socket timeout value, so we select
                if timeout is not None and timeout > 0.0:
                    read_ready, _, _ = select.select([socket], [], [], timeout)
                    if len(read_ready) == 0:
                        raise socket_.error(errno.EAGAIN, 'timed out')
                chunk = socket.recv(bytes_requested - len(data))
                data += chunk
                if chunk == b'':
                    if len(data) == 0:
                        if timeout is None:
                            return SecurityConst.errSSLClosedNoNotify
                        return SecurityConst.errSSLClosedAbort
                    break
        except (socket_.error) as e:
            error = e.errno

        if error is not None and error != errno.EAGAIN:
            if error == errno.ECONNRESET or error == errno.EPIPE:
                return SecurityConst.errSSLClosedNoNotify
            return SecurityConst.errSSLClosedAbort

        if self and not self._done_handshake:
            # SecureTransport doesn't bother to check if the TLS record header
            # is valid before asking to read more data, which can result in
            # connection hangs. Here we do basic checks to get around the issue.
            if len(data) >= 3 and len(self._server_hello) == 0:
                # Check to ensure it is an alert or handshake first
                valid_record_type = data[0:1] in set([b'\x15', b'\x16'])
                # Check if the protocol version is SSL 3.0 or TLS 1.0-1.3
                valid_protocol_version = data[1:3] in set([
                    b'\x03\x00',
                    b'\x03\x01',
                    b'\x03\x02',
                    b'\x03\x03',
                    b'\x03\x04'
                ])
                if not valid_record_type or not valid_protocol_version:
                    self._server_hello += data + _read_remaining(socket)
                    return SecurityConst.errSSLProtocol
            self._server_hello += data

        write_to_buffer(data_buffer, data)
        pointer_set(data_length_pointer, len(data))

        if len(data) != bytes_requested:
            return SecurityConst.errSSLWouldBlock

        return 0
    except (KeyboardInterrupt) as e:
        if self:
            self._exception = e
        return SecurityConst.errSSLClosedAbort
def write(self, data):
        """
        Writes data to the TLS-wrapped socket

        :param data:
            A byte string to write to the socket

        :raises:
            socket.socket - when a non-TLS socket error occurs
            oscrypto.errors.TLSError - when a TLS-related error occurs
            ValueError - when any of the parameters contain an invalid value
            TypeError - when any of the parameters are of the wrong type
            OSError - when an error is returned by the OS crypto library
        """

        if self._context_handle_pointer is None:
            self._raise_closed()

        if not self._encrypt_data_buffer:
            self._encrypt_data_buffer = buffer_from_bytes(self._header_size + self._message_size + self._trailer_size)
            self._encrypt_desc, self._encrypt_buffers = self._create_buffers(4)

            self._encrypt_buffers[0].BufferType = Secur32Const.SECBUFFER_STREAM_HEADER
            self._encrypt_buffers[0].cbBuffer = self._header_size
            self._encrypt_buffers[0].pvBuffer = cast(secur32, 'BYTE *', self._encrypt_data_buffer)

            self._encrypt_buffers[1].BufferType = Secur32Const.SECBUFFER_DATA
            self._encrypt_buffers[1].pvBuffer = ref(self._encrypt_data_buffer, self._header_size)

            self._encrypt_buffers[2].BufferType = Secur32Const.SECBUFFER_STREAM_TRAILER
            self._encrypt_buffers[2].cbBuffer = self._trailer_size
            self._encrypt_buffers[2].pvBuffer = ref(self._encrypt_data_buffer, self._header_size + self._message_size)

        while len(data) > 0:
            to_write = min(len(data), self._message_size)
            write_to_buffer(self._encrypt_data_buffer, data[0:to_write], self._header_size)

            self._encrypt_buffers[1].cbBuffer = to_write
            self._encrypt_buffers[2].pvBuffer = ref(self._encrypt_data_buffer, self._header_size + to_write)

            result = secur32.EncryptMessage(
                self._context_handle_pointer,
                0,
                self._encrypt_desc,
                0
            )

            if result != Secur32Const.SEC_E_OK:
                handle_error(result, TLSError)

            to_send = native(int, self._encrypt_buffers[0].cbBuffer)
            to_send += native(int, self._encrypt_buffers[1].cbBuffer)
            to_send += native(int, self._encrypt_buffers[2].cbBuffer)
            try:
                self._socket.send(bytes_from_buffer(self._encrypt_data_buffer, to_send))
            except (socket_.error) as e:
                if e.errno == 10053:
                    raise_disconnection()
                raise

            data = data[to_send:]
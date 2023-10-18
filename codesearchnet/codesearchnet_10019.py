def read(self, max_length):
        """
        Reads data from the TLS-wrapped socket

        :param max_length:
            The number of bytes to read

        :raises:
            socket.socket - when a non-TLS socket error occurs
            oscrypto.errors.TLSError - when a TLS-related error occurs
            ValueError - when any of the parameters contain an invalid value
            TypeError - when any of the parameters are of the wrong type
            OSError - when an error is returned by the OS crypto library

        :return:
            A byte string of the data read
        """

        if not isinstance(max_length, int_types):
            raise TypeError(pretty_message(
                '''
                max_length must be an integer, not %s
                ''',
                type_name(max_length)
            ))

        if self._context_handle_pointer is None:

            # Allow the user to read any remaining decrypted data
            if self._decrypted_bytes != b'':
                output = self._decrypted_bytes[0:max_length]
                self._decrypted_bytes = self._decrypted_bytes[max_length:]
                return output

            self._raise_closed()

        # The first time read is called, set up a single contiguous buffer that
        # it used by DecryptMessage() to populate the three output buffers.
        # Since we are creating the buffer, we do not need to free it other
        # than allowing Python to GC it once this object is GCed.
        if not self._decrypt_data_buffer:
            self._decrypt_data_buffer = buffer_from_bytes(self._buffer_size)
            self._decrypt_desc, self._decrypt_buffers = self._create_buffers(4)
            self._decrypt_buffers[0].BufferType = Secur32Const.SECBUFFER_DATA
            self._decrypt_buffers[0].pvBuffer = cast(secur32, 'BYTE *', self._decrypt_data_buffer)

        to_recv = max(max_length, self._buffer_size)

        # These variables are set to reduce dict access and function calls
        # in the read loop. Also makes the code easier to read.
        null_value = null()
        buf0 = self._decrypt_buffers[0]
        buf1 = self._decrypt_buffers[1]
        buf2 = self._decrypt_buffers[2]
        buf3 = self._decrypt_buffers[3]

        def _reset_buffers():
            buf0.BufferType = Secur32Const.SECBUFFER_DATA
            buf0.pvBuffer = cast(secur32, 'BYTE *', self._decrypt_data_buffer)
            buf0.cbBuffer = 0

            buf1.BufferType = Secur32Const.SECBUFFER_EMPTY
            buf1.pvBuffer = null_value
            buf1.cbBuffer = 0

            buf2.BufferType = Secur32Const.SECBUFFER_EMPTY
            buf2.pvBuffer = null_value
            buf2.cbBuffer = 0

            buf3.BufferType = Secur32Const.SECBUFFER_EMPTY
            buf3.pvBuffer = null_value
            buf3.cbBuffer = 0

        output = self._decrypted_bytes
        output_len = len(output)

        self._decrypted_bytes = b''

        # Don't block if we have buffered data available
        if output_len > 0 and not self.select_read(0):
            self._decrypted_bytes = b''
            return output

        # This read loop will only be run if there wasn't enough
        # buffered data to fulfill the requested max_length
        do_read = len(self._received_bytes) == 0

        while output_len < max_length:
            if do_read:
                self._received_bytes += self._socket.recv(to_recv)
                if len(self._received_bytes) == 0:
                    raise_disconnection()

            data_len = min(len(self._received_bytes), self._buffer_size)
            if data_len == 0:
                break
            self._decrypt_buffers[0].cbBuffer = data_len
            write_to_buffer(self._decrypt_data_buffer, self._received_bytes[0:data_len])

            result = secur32.DecryptMessage(
                self._context_handle_pointer,
                self._decrypt_desc,
                0,
                null()
            )

            do_read = False

            if result == Secur32Const.SEC_E_INCOMPLETE_MESSAGE:
                _reset_buffers()
                do_read = True
                continue

            elif result == Secur32Const.SEC_I_CONTEXT_EXPIRED:
                self._remote_closed = True
                self.shutdown()
                break

            elif result == Secur32Const.SEC_I_RENEGOTIATE:
                self._handshake(renegotiate=True)
                return self.read(max_length)

            elif result != Secur32Const.SEC_E_OK:
                handle_error(result, TLSError)

            valid_buffer_types = set([
                Secur32Const.SECBUFFER_EMPTY,
                Secur32Const.SECBUFFER_STREAM_HEADER,
                Secur32Const.SECBUFFER_STREAM_TRAILER
            ])
            extra_amount = None
            for buf in (buf0, buf1, buf2, buf3):
                buffer_type = buf.BufferType
                if buffer_type == Secur32Const.SECBUFFER_DATA:
                    output += bytes_from_buffer(buf.pvBuffer, buf.cbBuffer)
                    output_len = len(output)
                elif buffer_type == Secur32Const.SECBUFFER_EXTRA:
                    extra_amount = native(int, buf.cbBuffer)
                elif buffer_type not in valid_buffer_types:
                    raise OSError(pretty_message(
                        '''
                        Unexpected decrypt output buffer of type %s
                        ''',
                        buffer_type
                    ))

            if extra_amount:
                self._received_bytes = self._received_bytes[data_len - extra_amount:]
            else:
                self._received_bytes = self._received_bytes[data_len:]

            # Here we reset the structs for the next call to DecryptMessage()
            _reset_buffers()

            # If we have read something, but there is nothing left to read, we
            # break so that we don't block for longer than necessary
            if self.select_read(0):
                do_read = True

            if not do_read and len(self._received_bytes) == 0:
                break

        # If the output is more than we requested (because data is decrypted in
        # blocks), we save the extra in a buffer
        if len(output) > max_length:
            self._decrypted_bytes = output[max_length:]
            output = output[0:max_length]

        return output
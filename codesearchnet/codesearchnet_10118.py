def _os_buffered_size(self):
        """
        Returns the number of bytes of decrypted data stored in the Secure
        Transport read buffer. This amount of data can be read from SSLRead()
        without calling self._socket.recv().

        :return:
            An integer - the number of available bytes
        """

        num_bytes_pointer = new(Security, 'size_t *')
        result = Security.SSLGetBufferedReadSize(
            self._session_context,
            num_bytes_pointer
        )
        handle_sec_error(result)

        return deref(num_bytes_pointer)
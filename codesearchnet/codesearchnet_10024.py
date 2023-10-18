def shutdown(self):
        """
        Shuts down the TLS session and then shuts down the underlying socket

        :raises:
            OSError - when an error is returned by the OS crypto library
        """

        if self._context_handle_pointer is None:
            return

        out_buffers = None
        try:
            # ApplyControlToken fails with SEC_E_UNSUPPORTED_FUNCTION
            # when called on Windows 7
            if _win_version_info >= (6, 2):
                buffers = new(secur32, 'SecBuffer[1]')

                # This is a SCHANNEL_SHUTDOWN token (DWORD of 1)
                buffers[0].cbBuffer = 4
                buffers[0].BufferType = Secur32Const.SECBUFFER_TOKEN
                buffers[0].pvBuffer = cast(secur32, 'BYTE *', buffer_from_bytes(b'\x01\x00\x00\x00'))

                sec_buffer_desc_pointer = struct(secur32, 'SecBufferDesc')
                sec_buffer_desc = unwrap(sec_buffer_desc_pointer)

                sec_buffer_desc.ulVersion = Secur32Const.SECBUFFER_VERSION
                sec_buffer_desc.cBuffers = 1
                sec_buffer_desc.pBuffers = buffers

                result = secur32.ApplyControlToken(self._context_handle_pointer, sec_buffer_desc_pointer)
                handle_error(result, TLSError)

            out_sec_buffer_desc_pointer, out_buffers = self._create_buffers(2)
            out_buffers[0].BufferType = Secur32Const.SECBUFFER_TOKEN
            out_buffers[1].BufferType = Secur32Const.SECBUFFER_ALERT

            output_context_flags_pointer = new(secur32, 'ULONG *')

            result = secur32.InitializeSecurityContextW(
                self._session._credentials_handle,
                self._context_handle_pointer,
                self._hostname,
                self._context_flags,
                0,
                0,
                null(),
                0,
                null(),
                out_sec_buffer_desc_pointer,
                output_context_flags_pointer,
                null()
            )
            acceptable_results = set([
                Secur32Const.SEC_E_OK,
                Secur32Const.SEC_E_CONTEXT_EXPIRED,
                Secur32Const.SEC_I_CONTINUE_NEEDED
            ])
            if result not in acceptable_results:
                handle_error(result, TLSError)

            token = bytes_from_buffer(out_buffers[0].pvBuffer, out_buffers[0].cbBuffer)
            try:
                # If there is an error sending the shutdown, ignore it since the
                # connection is likely gone at this point
                self._socket.send(token)
            except (socket_.error):
                pass

        finally:
            if out_buffers:
                if not is_null(out_buffers[0].pvBuffer):
                    secur32.FreeContextBuffer(out_buffers[0].pvBuffer)
                if not is_null(out_buffers[1].pvBuffer):
                    secur32.FreeContextBuffer(out_buffers[1].pvBuffer)

            secur32.DeleteSecurityContext(self._context_handle_pointer)
            self._context_handle_pointer = None

            try:
                self._socket.shutdown(socket_.SHUT_RDWR)
            except (socket_.error):
                pass
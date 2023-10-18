def _stream_data(self, environ, content_length, block_size):
        """Get the data from a non-chunked transfer."""
        if content_length == 0:
            # TODO: review this
            # XP and Vista MiniRedir submit PUT with Content-Length 0,
            # before LOCK and the real PUT. So we have to accept this.
            _logger.info("PUT: Content-Length == 0. Creating empty file...")

        #        elif content_length < 0:
        #            # TODO: review this
        #            # If CONTENT_LENGTH is invalid, we may try to workaround this
        #            # by reading until the end of the stream. This may block however!
        #            # The iterator produced small chunks of varying size, but not
        #            # sure, if we always get everything before it times out.
        #            _logger.warning("PUT with invalid Content-Length (%s). "
        #                            "Trying to read all (this may timeout)..."
        #                            .format(environ.get("CONTENT_LENGTH")))
        #            nb = 0
        #            try:
        #                for s in environ["wsgi.input"]:
        #                    environ["wsgidav.some_input_read"] = 1
        #                    _logger.debug("PUT: read from wsgi.input.__iter__, len=%s" % len(s))
        #                    yield s
        #                    nb += len (s)
        #            except socket.timeout:
        #                _logger.warning("PUT: input timed out after writing %s bytes" % nb)
        #                hasErrors = True
        else:
            assert content_length > 0
            contentremain = content_length
            while contentremain > 0:
                n = min(contentremain, block_size)
                readbuffer = environ["wsgi.input"].read(n)
                # This happens with litmus expect-100 test:
                if not len(readbuffer) > 0:
                    _logger.error("input.read({}) returned 0 bytes".format(n))
                    break
                environ["wsgidav.some_input_read"] = 1
                yield readbuffer
                contentremain -= len(readbuffer)

            if contentremain == 0:
                environ["wsgidav.all_input_read"] = 1
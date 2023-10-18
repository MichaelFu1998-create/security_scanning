def _stream_data_chunked(self, environ, block_size):
        """Get the data from a chunked transfer."""
        # Chunked Transfer Coding
        # http://www.servlets.com/rfcs/rfc2616-sec3.html#sec3.6.1

        if "Darwin" in environ.get("HTTP_USER_AGENT", "") and environ.get(
            "HTTP_X_EXPECTED_ENTITY_LENGTH"
        ):
            # Mac Finder, that does not prepend chunk-size + CRLF ,
            # like it should to comply with the spec. It sends chunk
            # size as integer in a HTTP header instead.
            WORKAROUND_CHUNK_LENGTH = True
            buf = environ.get("HTTP_X_EXPECTED_ENTITY_LENGTH", "0")
            length = int(buf)
        else:
            WORKAROUND_CHUNK_LENGTH = False
            buf = environ["wsgi.input"].readline()
            environ["wsgidav.some_input_read"] = 1
            if buf == compat.b_empty:
                length = 0
            else:
                length = int(buf, 16)

        while length > 0:
            buf = environ["wsgi.input"].read(block_size)
            yield buf
            if WORKAROUND_CHUNK_LENGTH:
                environ["wsgidav.some_input_read"] = 1
                # Keep receiving until we read expected size or reach
                # EOF
                if buf == compat.b_empty:
                    length = 0
                else:
                    length -= len(buf)
            else:
                environ["wsgi.input"].readline()
                buf = environ["wsgi.input"].readline()
                if buf == compat.b_empty:
                    length = 0
                else:
                    length = int(buf, 16)
        environ["wsgidav.all_input_read"] = 1
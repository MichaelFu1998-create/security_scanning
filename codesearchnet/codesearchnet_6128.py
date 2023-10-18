def _send_resource(self, environ, start_response, is_head_method):
        """
        If-Range
            If the entity is unchanged, send me the part(s) that I am missing;
            otherwise, send me the entire new entity
            If-Range: "737060cd8c284d8af7ad3082f209582d"

        @see: http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.27
        """
        path = environ["PATH_INFO"]
        res = self._davProvider.get_resource_inst(path, environ)

        if util.get_content_length(environ) != 0:
            self._fail(
                HTTP_MEDIATYPE_NOT_SUPPORTED,
                "The server does not handle any body content.",
            )
        elif environ.setdefault("HTTP_DEPTH", "0") != "0":
            self._fail(HTTP_BAD_REQUEST, "Only Depth: 0 supported.")
        elif res is None:
            self._fail(HTTP_NOT_FOUND)
        elif res.is_collection:
            self._fail(
                HTTP_FORBIDDEN,
                "Directory browsing is not enabled."
                "(to enable it put WsgiDavDirBrowser into middleware_stack"
                "option and set dir_browser -> enabled = True option.)",
            )

        self._evaluate_if_headers(res, environ)

        filesize = res.get_content_length()
        if filesize is None:
            filesize = -1  # flag logic to read until EOF

        last_modified = res.get_last_modified()
        if last_modified is None:
            last_modified = -1

        entitytag = res.get_etag()
        if entitytag is None:
            entitytag = "[]"

        # Ranges
        doignoreranges = (
            not res.support_content_length()
            or not res.support_ranges()
            or filesize == 0
        )
        if (
            "HTTP_RANGE" in environ
            and "HTTP_IF_RANGE" in environ
            and not doignoreranges
        ):
            ifrange = environ["HTTP_IF_RANGE"]
            # Try as http-date first (Return None, if invalid date string)
            secstime = util.parse_time_string(ifrange)
            if secstime:
                if last_modified != secstime:
                    doignoreranges = True
            else:
                # Use as entity tag
                ifrange = ifrange.strip('" ')
                if entitytag is None or ifrange != entitytag:
                    doignoreranges = True

        ispartialranges = False
        if "HTTP_RANGE" in environ and not doignoreranges:
            ispartialranges = True
            list_ranges, _totallength = util.obtain_content_ranges(
                environ["HTTP_RANGE"], filesize
            )
            if len(list_ranges) == 0:
                # No valid ranges present
                self._fail(HTTP_RANGE_NOT_SATISFIABLE)

            # More than one range present -> take only the first range, since
            # multiple range returns require multipart, which is not supported
            # obtain_content_ranges supports more than one range in case the above
            # behaviour changes in future
            (range_start, range_end, range_length) = list_ranges[0]
        else:
            (range_start, range_end, range_length) = (0, filesize - 1, filesize)

        # Content Processing
        mimetype = res.get_content_type()  # provider.get_content_type(path)

        response_headers = []
        if res.support_content_length():
            # Content-length must be of type string
            response_headers.append(("Content-Length", str(range_length)))
        if res.support_modified():
            response_headers.append(
                ("Last-Modified", util.get_rfc1123_time(last_modified))
            )
        response_headers.append(("Content-Type", mimetype))
        response_headers.append(("Date", util.get_rfc1123_time()))
        if res.support_etag():
            response_headers.append(("ETag", '"{}"'.format(entitytag)))

        if "response_headers" in environ["wsgidav.config"]:
            customHeaders = environ["wsgidav.config"]["response_headers"]
            for header, value in customHeaders:
                response_headers.append((header, value))

        res.finalize_headers(environ, response_headers)

        if ispartialranges:
            # response_headers.append(("Content-Ranges", "bytes " + str(range_start) + "-" +
            #    str(range_end) + "/" + str(range_length)))
            response_headers.append(
                (
                    "Content-Range",
                    "bytes {}-{}/{}".format(range_start, range_end, filesize),
                )
            )
            start_response("206 Partial Content", response_headers)
        else:
            start_response("200 OK", response_headers)

        # Return empty body for HEAD requests
        if is_head_method:
            yield b""
            return

        fileobj = res.get_content()

        if not doignoreranges:
            fileobj.seek(range_start)

        contentlengthremaining = range_length
        while 1:
            if contentlengthremaining < 0 or contentlengthremaining > self.block_size:
                readbuffer = fileobj.read(self.block_size)
            else:
                readbuffer = fileobj.read(contentlengthremaining)
            assert compat.is_bytes(readbuffer)
            yield readbuffer
            contentlengthremaining -= len(readbuffer)
            if len(readbuffer) == 0 or contentlengthremaining == 0:
                break
        fileobj.close()
        return
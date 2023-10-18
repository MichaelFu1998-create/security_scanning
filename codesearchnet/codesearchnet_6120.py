def _send_response(
        self, environ, start_response, root_res, success_code, error_list
    ):
        """Send WSGI response (single or multistatus).

        - If error_list is None or [], then <success_code> is send as response.
        - If error_list contains a single error with a URL that matches root_res,
          then this error is returned.
        - If error_list contains more than one error, then '207 Multi-Status' is
          returned.
        """
        assert success_code in (HTTP_CREATED, HTTP_NO_CONTENT, HTTP_OK)
        if not error_list:
            # Status OK
            return util.send_status_response(environ, start_response, success_code)
        if len(error_list) == 1 and error_list[0][0] == root_res.get_href():
            # Only one error that occurred on the root resource
            return util.send_status_response(environ, start_response, error_list[0][1])

        # Multiple errors, or error on one single child
        multistatusEL = xml_tools.make_multistatus_el()

        for refurl, e in error_list:
            # assert refurl.startswith("http:")
            assert refurl.startswith("/")
            assert isinstance(e, DAVError)
            responseEL = etree.SubElement(multistatusEL, "{DAV:}response")
            etree.SubElement(responseEL, "{DAV:}href").text = refurl
            etree.SubElement(responseEL, "{DAV:}status").text = "HTTP/1.1 {}".format(
                get_http_status_string(e)
            )

        return util.send_multi_status_response(environ, start_response, multistatusEL)
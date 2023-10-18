def _evaluate_if_headers(self, res, environ):
        """Apply HTTP headers on <path>, raising DAVError if conditions fail.

        Add environ['wsgidav.conditions.if'] and environ['wsgidav.ifLockTokenList'].
        Handle these headers:

          - If-Match, If-Modified-Since, If-None-Match, If-Unmodified-Since:
            Raising HTTP_PRECONDITION_FAILED or HTTP_NOT_MODIFIED
          - If:
            Raising HTTP_PRECONDITION_FAILED

        @see http://www.webdav.org/specs/rfc4918.html#HEADER_If
        @see util.evaluate_http_conditionals
        """
        # Add parsed If header to environ
        if "wsgidav.conditions.if" not in environ:
            util.parse_if_header_dict(environ)

        # Bail out, if res does not exist
        if res is None:
            return

        ifDict = environ["wsgidav.conditions.if"]

        # Raise HTTP_PRECONDITION_FAILED or HTTP_NOT_MODIFIED, if standard
        # HTTP condition fails
        last_modified = -1  # nonvalid modified time
        entitytag = "[]"  # Non-valid entity tag
        if res.get_last_modified() is not None:
            last_modified = res.get_last_modified()
        if res.get_etag() is not None:
            entitytag = res.get_etag()

        if (
            "HTTP_IF_MODIFIED_SINCE" in environ
            or "HTTP_IF_UNMODIFIED_SINCE" in environ
            or "HTTP_IF_MATCH" in environ
            or "HTTP_IF_NONE_MATCH" in environ
        ):
            util.evaluate_http_conditionals(res, last_modified, entitytag, environ)

        if "HTTP_IF" not in environ:
            return

        # Raise HTTP_PRECONDITION_FAILED, if DAV 'If' condition fails
        # TODO: handle empty locked resources
        # TODO: handle unmapped locked resources
        #            isnewfile = not provider.exists(mappedpath)

        refUrl = res.get_ref_url()
        lockMan = self._davProvider.lock_manager
        locktokenlist = []
        if lockMan:
            lockList = lockMan.get_indirect_url_lock_list(
                refUrl, environ["wsgidav.user_name"]
            )
            for lock in lockList:
                locktokenlist.append(lock["token"])

        if not util.test_if_header_dict(res, ifDict, refUrl, locktokenlist, entitytag):
            self._fail(HTTP_PRECONDITION_FAILED, "'If' header condition failed.")

        return
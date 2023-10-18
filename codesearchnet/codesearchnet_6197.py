def evaluate_http_conditionals(dav_res, last_modified, entitytag, environ):
    """Handle 'If-...:' headers (but not 'If:' header).

    If-Match
        @see: http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.24
        Only perform the action if the client supplied entity matches the
        same entity on the server. This is mainly for methods like
        PUT to only update a resource if it has not been modified since the
        user last updated it.
        If-Match: "737060cd8c284d8af7ad3082f209582d"
    If-Modified-Since
        @see: http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.25
        Allows a 304 Not Modified to be returned if content is unchanged
        If-Modified-Since: Sat, 29 Oct 1994 19:43:31 GMT
    If-None-Match
        @see: http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.26
        Allows a 304 Not Modified to be returned if content is unchanged,
        see HTTP ETag
        If-None-Match: "737060cd8c284d8af7ad3082f209582d"
    If-Unmodified-Since
        @see: http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.28
        Only send the response if the entity has not been modified since a
        specific time.
    """
    if not dav_res:
        return
    # Conditions

    # An HTTP/1.1 origin server, upon receiving a conditional request that includes both a
    # Last-Modified date (e.g., in an If-Modified-Since or If-Unmodified-Since header field) and
    # one or more entity tags (e.g., in an If-Match, If-None-Match, or If-Range header field) as
    # cache validators, MUST NOT return a response status of 304 (Not Modified) unless doing so
    # is consistent with all of the conditional header fields in the request.

    if "HTTP_IF_MATCH" in environ and dav_res.support_etag():
        ifmatchlist = environ["HTTP_IF_MATCH"].split(",")
        for ifmatchtag in ifmatchlist:
            ifmatchtag = ifmatchtag.strip(' "\t')
            if ifmatchtag == entitytag or ifmatchtag == "*":
                break
            raise DAVError(HTTP_PRECONDITION_FAILED, "If-Match header condition failed")

    # TODO: after the refactoring
    ifModifiedSinceFailed = False
    if "HTTP_IF_MODIFIED_SINCE" in environ and dav_res.support_modified():
        ifmodtime = parse_time_string(environ["HTTP_IF_MODIFIED_SINCE"])
        if ifmodtime and ifmodtime > last_modified:
            ifModifiedSinceFailed = True

    # If-None-Match
    # If none of the entity tags match, then the server MAY perform the requested method as if the
    # If-None-Match header field did not exist, but MUST also ignore any If-Modified-Since header
    # field (s) in the request. That is, if no entity tags match, then the server MUST NOT return
    # a 304 (Not Modified) response.
    ignoreIfModifiedSince = False
    if "HTTP_IF_NONE_MATCH" in environ and dav_res.support_etag():
        ifmatchlist = environ["HTTP_IF_NONE_MATCH"].split(",")
        for ifmatchtag in ifmatchlist:
            ifmatchtag = ifmatchtag.strip(' "\t')
            if ifmatchtag == entitytag or ifmatchtag == "*":
                # ETag matched. If it's a GET request and we don't have an
                # conflicting If-Modified header, we return NOT_MODIFIED
                if (
                    environ["REQUEST_METHOD"] in ("GET", "HEAD")
                    and not ifModifiedSinceFailed
                ):
                    raise DAVError(HTTP_NOT_MODIFIED, "If-None-Match header failed")
                raise DAVError(
                    HTTP_PRECONDITION_FAILED, "If-None-Match header condition failed"
                )
        ignoreIfModifiedSince = True

    if "HTTP_IF_UNMODIFIED_SINCE" in environ and dav_res.support_modified():
        ifunmodtime = parse_time_string(environ["HTTP_IF_UNMODIFIED_SINCE"])
        if ifunmodtime and ifunmodtime <= last_modified:
            raise DAVError(
                HTTP_PRECONDITION_FAILED, "If-Unmodified-Since header condition failed"
            )

    if ifModifiedSinceFailed and not ignoreIfModifiedSince:
        raise DAVError(HTTP_NOT_MODIFIED, "If-Modified-Since header condition failed")

    return
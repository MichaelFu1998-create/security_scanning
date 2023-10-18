def error_handler(req):
    """ Error handler for HTTP requests
    """
    error_codes = {
        400: ze.UnsupportedParams,
        401: ze.UserNotAuthorised,
        403: ze.UserNotAuthorised,
        404: ze.ResourceNotFound,
        409: ze.Conflict,
        412: ze.PreConditionFailed,
        413: ze.RequestEntityTooLarge,
        428: ze.PreConditionRequired,
        429: ze.TooManyRequests,
    }

    def err_msg(req):
        """ Return a nicely-formatted error message
        """
        return "\nCode: %s\nURL: %s\nMethod: %s\nResponse: %s" % (
            req.status_code,
            # error.msg,
            req.url,
            req.request.method,
            req.text,
        )

    if error_codes.get(req.status_code):
        # check to see whether its 429
        if req.status_code == 429:
            # call our back-off function
            delay = backoff.delay
            if delay > 32:
                # we've waited a total of 62 seconds (2 + 4 … + 32), so give up
                backoff.reset()
                raise ze.TooManyRetries(
                    "Continuing to receive HTTP 429 \
responses after 62 seconds. You are being rate-limited, try again later"
                )
            time.sleep(delay)
            sess = requests.Session()
            new_req = sess.send(req.request)
            try:
                new_req.raise_for_status()
            except requests.exceptions.HTTPError:
                error_handler(new_req)
        else:
            raise error_codes.get(req.status_code)(err_msg(req))
    else:
        raise ze.HTTPError(err_msg(req))
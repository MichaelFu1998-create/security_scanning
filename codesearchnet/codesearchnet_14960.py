def _with_error_handling(resp, error, mode, response_format):
        """
        Static method for error handling.

        :param resp - API response
        :param error - Error thrown
        :param mode - Error mode
        :param response_format - XML or json
        """
        def safe_parse(r):
            try:
                return APIWrapper._parse_resp(r, response_format)
            except (ValueError, SyntaxError) as ex:
                log.error(ex)
                r.parsed = None
                return r

        if isinstance(error, requests.HTTPError):
            if resp.status_code == 400:
                # It means that request parameters were rejected by the server,
                # so we need to enrich standard error message
                # with 'ValidationErrors'
                # from the response
                resp = safe_parse(resp)
                if resp.parsed is not None:
                    parsed_resp = resp.parsed
                    messages = []
                    if response_format == 'xml' and\
                            parsed_resp.find('./ValidationErrors') is not None:
                        messages = [e.find('./Message').text
                                    for e in parsed_resp.findall('./ValidationErrors/ValidationErrorDto')]
                    elif response_format == 'json' and 'ValidationErrors' in parsed_resp:
                        messages = [e['Message']
                                    for e in parsed_resp['ValidationErrors']]
                    error = requests.HTTPError(
                        '%s: %s' % (error, '\n\t'.join(messages)), response=resp)
            elif resp.status_code == 429:
                error = requests.HTTPError('%sToo many requests in the last minute.' % error,
                                           response=resp)

        if STRICT == mode:
            raise error
        elif GRACEFUL == mode:
            if isinstance(error, EmptyResponse):
                # Empty response is returned by the API occasionally,
                # in this case it makes sense to ignore it and retry.
                log.warning(error)
                resp.parsed = None
                return resp

            elif isinstance(error, requests.HTTPError):
                # Ignoring 'Too many requests' error,
                # since subsequent retries will come after a delay.
                if resp.status_code == 429:    # Too many requests
                    log.warning(error)
                    return safe_parse(resp)
                else:
                    raise error
            else:
                raise error
        else:
            # ignore everything, just log it and return whatever response we
            # have
            log.error(error)
            return safe_parse(resp)
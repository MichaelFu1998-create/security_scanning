def _query(self, endpoint, path=None, query=None,
               order_by=None, limit=None, offset=None, include_total=False,
               summarize_by=None, count_by=None, count_filter=None,
               request_method='GET'):
        """This method actually querries PuppetDB. Provided an endpoint and an
        optional path and/or query it will fire a request at PuppetDB. If
        PuppetDB can be reached and answers within the timeout we'll decode
        the response and give it back or raise for the HTTP Status Code
        PuppetDB gave back.

        :param endpoint: The PuppetDB API endpoint we want to query.
        :type endpoint: :obj:`string`
        :param path: An additional path if we don't wish to query the\
                bare endpoint.
        :type path: :obj:`string`
        :param query: (optional) A query to further narrow down the resultset.
        :type query: :obj:`string`
        :param order_by: (optional) Set the order parameters for the resultset.
        :type order_by: :obj:`string`
        :param limit: (optional) Tell PuppetDB to limit it's response to this\
                number of objects.
        :type limit: :obj:`int`
        :param offset: (optional) Tell PuppetDB to start it's response from\
                the given offset. This is useful for implementing pagination\
                but is not supported just yet.
        :type offset: :obj:`string`
        :param include_total: (optional) Include the total number of results
        :type order_by: :obj:`bool`
        :param summarize_by: (optional) Specify what type of object you'd like\
                to see counts at the event-counts and aggregate-event-counts \
                endpoints
        :type summarize_by: :obj:`string`
        :param count_by: (optional) Specify what type of object is counted
        :type count_by: :obj:`string`
        :param count_filter: (optional) Specify a filter for the results
        :type count_filter: :obj:`string`

        :raises: :class:`~pypuppetdb.errors.EmptyResponseError`

        :returns: The decoded response from PuppetDB
        :rtype: :obj:`dict` or :obj:`list`
        """
        log.debug('_query called with endpoint: {0}, path: {1}, query: {2}, '
                  'limit: {3}, offset: {4}, summarize_by {5}, count_by {6}, '
                  'count_filter: {7}'.format(endpoint, path, query, limit,
                                             offset, summarize_by, count_by,
                                             count_filter))

        url = self._url(endpoint, path=path)

        payload = {}
        if query is not None:
            payload['query'] = query
        if order_by is not None:
            payload[PARAMETERS['order_by']] = order_by
        if limit is not None:
            payload['limit'] = limit
        if include_total is True:
            payload[PARAMETERS['include_total']] = \
                json.dumps(include_total)
        if offset is not None:
            payload['offset'] = offset
        if summarize_by is not None:
            payload[PARAMETERS['summarize_by']] = summarize_by
        if count_by is not None:
            payload[PARAMETERS['count_by']] = count_by
        if count_filter is not None:
            payload[PARAMETERS['counts_filter']] = count_filter

        if not (payload):
            payload = None

        if not self.token:
            auth = (self.username, self.password)
        else:
            auth = None

        try:
            if request_method.upper() == 'GET':
                r = self._session.get(url, params=payload,
                                      verify=self.ssl_verify,
                                      cert=(self.ssl_cert, self.ssl_key),
                                      timeout=self.timeout,
                                      auth=auth)
            elif request_method.upper() == 'POST':
                r = self._session.post(url,
                                       data=json.dumps(payload, default=str),
                                       verify=self.ssl_verify,
                                       cert=(self.ssl_cert, self.ssl_key),
                                       timeout=self.timeout,
                                       auth=auth)
            else:
                log.error("Only GET or POST supported, {0} unsupported".format(
                          request_method))
                raise APIError
            r.raise_for_status()

            # get total number of results if requested with include-total
            # just a quick hack - needs improvement
            if 'X-Records' in r.headers:
                self.last_total = r.headers['X-Records']
            else:
                self.last_total = None

            json_body = r.json()
            if json_body is not None:
                return json_body
            else:
                del json_body
                raise EmptyResponseError

        except requests.exceptions.Timeout:
            log.error("{0} {1}:{2} over {3}.".format(ERROR_STRINGS['timeout'],
                                                     self.host, self.port,
                                                     self.protocol.upper()))
            raise
        except requests.exceptions.ConnectionError:
            log.error("{0} {1}:{2} over {3}.".format(ERROR_STRINGS['refused'],
                                                     self.host, self.port,
                                                     self.protocol.upper()))
            raise
        except requests.exceptions.HTTPError as err:
            log.error("{0} {1}:{2} over {3}.".format(err.response.text,
                                                     self.host, self.port,
                                                     self.protocol.upper()))
            raise
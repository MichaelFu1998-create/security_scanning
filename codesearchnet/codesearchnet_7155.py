async def fetch(self, method, url, params=None, headers=None, data=None):
        """Make an HTTP request.

        Automatically uses configured HTTP proxy, and adds Google authorization
        header and cookies.

        Failures will be retried MAX_RETRIES times before raising NetworkError.

        Args:
            method (str): Request method.
            url (str): Request URL.
            params (dict): (optional) Request query string parameters.
            headers (dict): (optional) Request headers.
            data: (str): (optional) Request body data.

        Returns:
            FetchResponse: Response data.

        Raises:
            NetworkError: If the request fails.
        """
        logger.debug('Sending request %s %s:\n%r', method, url, data)
        for retry_num in range(MAX_RETRIES):
            try:
                async with self.fetch_raw(method, url, params=params,
                                          headers=headers, data=data) as res:
                    async with async_timeout.timeout(REQUEST_TIMEOUT):
                        body = await res.read()
                logger.debug('Received response %d %s:\n%r',
                             res.status, res.reason, body)
            except asyncio.TimeoutError:
                error_msg = 'Request timed out'
            except aiohttp.ServerDisconnectedError as err:
                error_msg = 'Server disconnected error: {}'.format(err)
            except (aiohttp.ClientError, ValueError) as err:
                error_msg = 'Request connection error: {}'.format(err)
            else:
                break
            logger.info('Request attempt %d failed: %s', retry_num, error_msg)
        else:
            logger.info('Request failed after %d attempts', MAX_RETRIES)
            raise exceptions.NetworkError(error_msg)

        if res.status != 200:
            logger.info('Request returned unexpected status: %d %s',
                        res.status, res.reason)
            raise exceptions.NetworkError(
                'Request return unexpected status: {}: {}'
                .format(res.status, res.reason)
            )

        return FetchResponse(res.status, body)
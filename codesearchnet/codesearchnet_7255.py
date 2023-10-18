async def _longpoll_request(self):
        """Open a long-polling request and receive arrays.

        This method uses keep-alive to make re-opening the request faster, but
        the remote server will set the "Connection: close" header once an hour.

        Raises hangups.NetworkError or ChannelSessionError.
        """
        params = {
            'VER': 8,  # channel protocol version
            'gsessionid': self._gsessionid_param,
            'RID': 'rpc',  # request identifier
            't': 1,  # trial
            'SID': self._sid_param,  # session ID
            'CI': 0,  # 0 if streaming/chunked requests should be used
            'ctype': 'hangouts',  # client type
            'TYPE': 'xmlhttp',  # type of request
        }
        logger.info('Opening new long-polling request')
        try:
            async with self._session.fetch_raw('GET', CHANNEL_URL,
                                               params=params) as res:

                if res.status != 200:
                    if res.status == 400 and res.reason == 'Unknown SID':
                        raise ChannelSessionError('SID became invalid')
                    raise exceptions.NetworkError(
                        'Request return unexpected status: {}: {}'.format(
                            res.status, res.reason))

                while True:
                    async with async_timeout.timeout(PUSH_TIMEOUT):
                        chunk = await res.content.read(MAX_READ_BYTES)
                    if not chunk:
                        break

                    await self._on_push_data(chunk)

        except asyncio.TimeoutError:
            raise exceptions.NetworkError('Request timed out')
        except aiohttp.ServerDisconnectedError as err:
            raise exceptions.NetworkError(
                'Server disconnected error: %s' % err)
        except aiohttp.ClientPayloadError:
            raise ChannelSessionError('SID is about to expire')
        except aiohttp.ClientError as err:
            raise exceptions.NetworkError('Request connection error: %s' % err)
async def request(self, method, url, future,
                      headers=None,
                      session=None,
                      encoding=None,
                      **kwargs):
        """
            Make requests to the REST API

        Parameters
        ----------
        future : asyncio.Future
            Future used to return the response
        method : str
            Method to be used by the request
        url : str
            URL of the resource
        headers : .oauth.PeonyHeaders
            Custom headers (doesn't overwrite `Authorization` headers)
        session : aiohttp.ClientSession, optional
            Client session used to make the request

        Returns
        -------
        data.PeonyResponse
            Response to the request
        """
        await self.setup

        # prepare request arguments, particularly the headers
        req_kwargs = await self.headers.prepare_request(
            method=method,
            url=url,
            headers=headers,
            proxy=self.proxy,
            **kwargs
        )

        if encoding is None:
            encoding = self.encoding

        session = session if (session is not None) else self._session

        logger.debug("making request with parameters: %s" % req_kwargs)

        async with session.request(**req_kwargs) as response:
            if response.status < 400:
                data = await data_processing.read(response, self._loads,
                                                  encoding=encoding)

                future.set_result(data_processing.PeonyResponse(
                    data=data,
                    headers=response.headers,
                    url=response.url,
                    request=req_kwargs
                ))
            else:  # throw exception if status is not 2xx
                await exceptions.throw(response, loads=self._loads,
                                       encoding=encoding, url=url)
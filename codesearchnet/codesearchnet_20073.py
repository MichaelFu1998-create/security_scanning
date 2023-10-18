async def execute_method(self, method, **params):
        """Execute a specified Slack Web API method.

        Arguments:
          method (:py:class:`str`): The name of the method.
          **params (:py:class:`dict`): Any additional parameters
            required.

        Returns:
          :py:class:`dict`: The JSON data from the response.

        Raises:
          :py:class:`aiohttp.web_exceptions.HTTPException`: If the HTTP
            request returns a code other than 200 (OK).
          SlackApiError: If the Slack API is reached but the response
           contains an error message.

        """
        url = self.url_builder(method, url_params=params)
        logger.info('Executing method %r', method)
        response = await aiohttp.get(url)
        logger.info('Status: %r', response.status)
        if response.status == 200:
            json = await response.json()
            logger.debug('...with JSON %r', json)
            if json.get('ok'):
                return json
            raise SlackApiError(json['error'])
        else:
            raise_for_status(response)
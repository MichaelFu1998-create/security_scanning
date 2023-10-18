async def _execute(self, document, variable_values=None, retry=2):
        """Execute gql."""
        query_str = print_ast(document)
        payload = {"query": query_str, "variables": variable_values or {}}

        post_args = {
            "headers": {"Authorization": "Bearer " + self._access_token},
            "data": payload,
        }

        try:
            with async_timeout.timeout(self._timeout):
                resp = await self.websession.post(API_ENDPOINT, **post_args)
            if resp.status != 200:
                _LOGGER.error("Error connecting to Tibber, resp code: %s", resp.status)
                return None
            result = await resp.json()
        except aiohttp.ClientError as err:
            _LOGGER.error("Error connecting to Tibber: %s ", err, exc_info=True)
            if retry > 0:
                return await self._execute(document, variable_values, retry - 1)
            raise
        except asyncio.TimeoutError as err:
            _LOGGER.error(
                "Timed out when connecting to Tibber: %s ", err, exc_info=True
            )
            if retry > 0:
                return await self._execute(document, variable_values, retry - 1)
            raise
        errors = result.get("errors")
        if errors:
            _LOGGER.error("Received non-compatible response %s", errors)
        return result
async def call_on_response(self, data):
        """
        Try to fill the gaps and strip last tweet from the response
        if its id is that of the first tweet of the last response

        Parameters
        ----------
        data : list
            The response data
        """
        since_id = self.kwargs.get(self.param, 0) + 1

        if self.fill_gaps:
            if data[-1]['id'] != since_id:
                max_id = data[-1]['id'] - 1
                responses = with_max_id(self.request(**self.kwargs,
                                                     max_id=max_id))

                async for tweets in responses:
                    data.extend(tweets)

            if data[-1]['id'] == self.last_id:
                data = data[:-1]

        if not data and not self.force:
            raise StopAsyncIteration

        await self.set_param(data)
async def connect(self):
        '''Connect to a Pusher websocket
        '''
        if not self._consumer:
            waiter = self._waiter = asyncio.Future()
            try:
                address = self._websocket_host()
                self.logger.info('Connect to %s', address)
                self._consumer = await self.http.get(address)
                if self._consumer.status_code != 101:
                    raise PusherError("Could not connect to websocket")
            except Exception as exc:
                waiter.set_exception(exc)
                raise
            else:
                await waiter
        return self._consumer
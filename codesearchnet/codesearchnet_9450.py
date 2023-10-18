async def close(self):
        """
        :py:func:`asyncio.coroutine`

        Shutdown the server and close all connections.
        """
        self.server.close()
        tasks = [self.server.wait_closed()]
        for connection in self.connections.values():
            connection._dispatcher.cancel()
            tasks.append(connection._dispatcher)
        logger.info("waiting for %d tasks", len(tasks))
        await asyncio.wait(tasks)
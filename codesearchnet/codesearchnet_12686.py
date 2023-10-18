async def close(self):
        """ properly close the client """
        tasks = self._get_close_tasks()

        if tasks:
            await asyncio.wait(tasks)

        self._session = None
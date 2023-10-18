async def run_tasks(self):
        """ Run the tasks attached to the instance """
        tasks = self.get_tasks()
        self._gathered_tasks = asyncio.gather(*tasks, loop=self.loop)
        try:
            await self._gathered_tasks
        except CancelledError:
            pass
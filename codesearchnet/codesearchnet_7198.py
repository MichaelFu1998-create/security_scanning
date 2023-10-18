async def fire(self, *args, **kwargs):
        """Fire this event, calling all observers with the same arguments."""
        logger.debug('Fired {}'.format(self))
        for observer in self._observers:
            gen = observer(*args, **kwargs)
            if asyncio.iscoroutinefunction(observer):
                await gen
async def play_at(self, index: int):
        """ Play the queue from a specific point. Disregards tracks before the index. """
        self.queue = self.queue[min(index, len(self.queue) - 1):len(self.queue)]
        await self.play(ignore_shuffle=True)
async def play_previous(self):
        """ Plays previous track if it exist, if it doesn't raises a NoPreviousTrack error. """
        if not self.previous:
            raise NoPreviousTrack
        self.queue.insert(0, self.previous)
        await self.play(ignore_shuffle=True)
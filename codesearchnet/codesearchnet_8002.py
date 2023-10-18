async def play(self, track_index: int = 0, ignore_shuffle: bool = False):
        """ Plays the first track in the queue, if any or plays a track from the specified index in the queue. """
        if self.repeat and self.current:
            self.queue.append(self.current)

        self.previous = self.current
        self.current = None
        self.position = 0
        self.paused = False

        if not self.queue:
            await self.stop()
            await self._lavalink.dispatch_event(QueueEndEvent(self))
        else:
            if self.shuffle and not ignore_shuffle:
                track = self.queue.pop(randrange(len(self.queue)))
            else:
                track = self.queue.pop(min(track_index, len(self.queue) - 1))

            self.current = track
            await self._lavalink.ws.send(op='play', guildId=self.guild_id, track=track.track)
            await self._lavalink.dispatch_event(TrackStartEvent(self, track))
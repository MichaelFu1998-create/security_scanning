def add_next(self, requester: int, track: dict):
        """ Adds a track to beginning of the queue """
        self.queue.insert(0, AudioTrack().build(track, requester))
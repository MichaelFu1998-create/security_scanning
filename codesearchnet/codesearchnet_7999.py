def add(self, requester: int, track: dict):
        """ Adds a track to the queue. """
        self.queue.append(AudioTrack().build(track, requester))
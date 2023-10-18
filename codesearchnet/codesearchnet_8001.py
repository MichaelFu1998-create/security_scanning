def add_at(self, index: int, requester: int, track: dict):
        """ Adds a track at a specific index in the queue. """
        self.queue.insert(min(index, len(self.queue) - 1), AudioTrack().build(track, requester))
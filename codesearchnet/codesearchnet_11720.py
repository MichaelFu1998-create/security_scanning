def get_thumbprint(self):
        """
        Calculates the current thumbprint of the item being tracked.
        """
        d = {}
        for tracker in self.trackers:
            d[type(tracker).__name__] = tracker.get_thumbprint()
        return d
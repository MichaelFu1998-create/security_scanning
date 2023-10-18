def n_subscribers(self):
        """
        Returns the number of connected subscribers.

        :rtype:  int
        :returns: The number of subscribers.
        """
        hard = self.hard_subscribers and len(self.hard_subscribers) or 0
        weak = self.weak_subscribers and len(self.weak_subscribers) or 0
        return hard + weak
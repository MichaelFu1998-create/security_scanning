def _try_disconnect(self, ref):
        """
        Called by the weak reference when its target dies.
        In other words, we can assert that self.weak_subscribers is not
        None at this time.
        """
        with self.lock:
            weak = [s[0] for s in self.weak_subscribers]
            try:
                index = weak.index(ref)
            except ValueError:
                # subscriber was already removed by a call to disconnect()
                pass
            else:
                self.weak_subscribers.pop(index)
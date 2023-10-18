def once(self, event, listener):
        """Add a listener that is only called once."""
        self.emit('new_listener', event, listener)
        self._once[event].append(listener)
        self._check_limit(event)
        return self
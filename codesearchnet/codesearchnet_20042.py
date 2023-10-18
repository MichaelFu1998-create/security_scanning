def _check_limit(self, event):
        """Check if the listener limit is hit and warn if needed."""
        if self.count(event) > self.max_listeners:

            warnings.warn(
                'Too many listeners for event {}'.format(event),
                ResourceWarning,
            )
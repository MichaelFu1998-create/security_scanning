def update_state(self):
        """Update current status of the item and compute time of the next
        state change.

        :return: the new state.
        :returntype: :std:`datetime`"""
        self._lock.acquire()
        try:
            now = datetime.utcnow()
            if self.state == 'new':
                self.state = 'fresh'
            if self.state == 'fresh':
                if now > self.freshness_time:
                    self.state = 'old'
            if self.state == 'old':
                if now > self.expire_time:
                    self.state = 'stale'
            if self.state == 'stale':
                if now > self.purge_time:
                    self.state = 'purged'
            self.state_value = _state_values[self.state]
            return self.state
        finally:
            self._lock.release()
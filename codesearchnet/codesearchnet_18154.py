def subscribe(self, event, bet_ids):
        '''Subscribe to event for given bet ids.'''
        if not self._subscriptions.get(event):
            self._subscriptions[event] = set()
        self._subscriptions[event] = self._subscriptions[event].union(bet_ids)
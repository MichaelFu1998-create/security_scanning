def put(self, state_id):
        """ Enqueue it for processing """
        self._states.append(state_id)
        self._lock.notify_all()
        return state_id
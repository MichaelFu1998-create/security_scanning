def enqueue(self, state):
        """
            Enqueue state.
            Save state on storage, assigns an id to it, then add it to the
            priority queue
        """
        # save the state to secondary storage
        state_id = self._workspace.save_state(state)
        self.put(state_id)
        self._publish('did_enqueue_state', state_id, state)
        return state_id
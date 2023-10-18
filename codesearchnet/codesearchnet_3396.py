def _add_state_callback(self, state_id, state):
        """ Save summarize(state) on policy shared context before
            the state is stored
        """
        summary = self.summarize(state)
        if summary is None:
            return
        with self.locked_context('summaries', dict) as ctx:
            ctx[state_id] = summary
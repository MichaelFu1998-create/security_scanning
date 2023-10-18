def restore_state(self, system):
        """Called after unpickling to restore some attributes manually."""

        for space in self._spaces.values():
            space.restore_state(system)
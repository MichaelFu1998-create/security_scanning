def restore_state(self, system):
        """Called after unpickling to restore some attributes manually."""
        super().restore_state(system)
        BaseSpaceContainerImpl.restore_state(self, system)

        for cells in self._cells.values():
            cells.restore_state(system)
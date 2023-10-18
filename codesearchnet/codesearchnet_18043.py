def check_update_J(self):
        """
        Checks if the full J should be updated.

        Right now, just updates after update_J_frequency loops
        """
        self._J_update_counter += 1
        update = self._J_update_counter >= self.update_J_frequency
        return update & (not self._fresh_JTJ)
def _setstate(self, value, force=False):
        """
        Setting force to True allows for changing a state after it
        COMPLETED. This would otherwise be invalid.
        """
        if self._state == value:
            return
        if value < self._state and not force:
            raise WorkflowException(self.task_spec,
                                    'state went from %s to %s!' % (
                                        self.get_state_name(),
                                        self.state_names[value]))
        if __debug__:
            old = self.get_state_name()
        self._state = value
        if __debug__:
            self.log.append("Moving '%s' from %s to %s" % (
                self.get_name(),
                old, self.get_state_name()))
        self.state_history.append(value)
        LOG.debug("Moving '%s' (spec=%s) from %s to %s" % (
            self.get_name(),
            self.task_spec.name, old, self.get_state_name()))
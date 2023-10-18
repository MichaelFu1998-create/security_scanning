def trigger_update(self, params, values):
        """ Notify parent of a parameter change """
        if self._parent:
            self._parent.trigger_update(params, values)
        else:
            self.update(params, values)
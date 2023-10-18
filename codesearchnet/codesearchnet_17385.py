def _getActions(self):
        """Retrieve a list of actions supported by the object."""
        actions = _a11y.AXUIElement._getActions(self)
        # strip leading AX from actions - help distinguish them from attributes
        return [action[2:] for action in actions]
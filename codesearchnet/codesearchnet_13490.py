def set_action(self,action):
        """Set the action of the item.

        :Parameters:
            - `action`: the new action or `None`.
        :Types:
            - `action`: `unicode`
        """
        if action is None:
            if self.xmlnode.hasProp("action"):
                self.xmlnode.unsetProp("action")
            return
        if action not in ("remove","update"):
            raise ValueError("Action must be 'update' or 'remove'")
        action = unicode(action)
        self.xmlnode.setProp("action", action.encode("utf-8"))
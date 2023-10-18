def next_state(self, rule=None):
        """Proceeds to the next step in the flow.  Calls the associated
        :func:`Rule.on_leave` method for the for the current rule and the
        :func:`Rule.on_enter` for the rule being entered.  If the current step
        in the flow is multipath then a valid :class:`Rule` subclass must be
        passed into this call.  

        If there is only one possible path in the flow and a :class:`Rule` is
        given it will be ignored.

        :param rule: 
            if the current :class:`Rule` in the :class:`Flow` is multipath
            then the next :class:`Rule` in the flow must be provided.
        """
        num_kids = self.current_node.children.count()
        next_node = None
        if num_kids == 0:
            raise AttributeError('No next state in this Flow id=%s' % (
                self.flow.id))
        elif num_kids == 1:
            next_node = self.current_node.children.first()
        else:
            if not rule:
                raise AttributeError(('Current Rule %s is multipath but no '
                    'choice was passed in') % self.current_node.data.rule_name)

            for node in self.current_node.children.all():
                if node.data.rule_label == rule.class_label:
                    next_node = node
                    break

            if not next_node:
                raise AttributeError(('Current Rule %s is multipath and the '
                    'Rule choice passed in was not in the Flow') % (
                    self.current_node.data.rule_name))

        self.current_node.data.rule.on_leave(self)
        next_node.data.rule.on_enter(self)
        self.current_node = next_node
        self.save()
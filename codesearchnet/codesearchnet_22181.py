def _child_allowed(self, child_rule):
        """Called to verify that the given rule can become a child of the
        current node.  

        :raises AttributeError: 
            if the child is not allowed
        """
        num_kids = self.node.children.count()
        num_kids_allowed = len(self.rule.children)
        if not self.rule.multiple_paths:
            num_kids_allowed = 1

        if num_kids >= num_kids_allowed:
            raise AttributeError('Rule %s only allows %s children' % (
                self.rule_name, self.num_kids_allowed))

        # verify not a duplicate
        for node in self.node.children.all():
            if node.data.rule_label == child_rule.class_label:
                raise AttributeError('Child rule already exists')

        # check if the given rule is allowed as a child
        if child_rule not in self.rule.children:
            raise AttributeError('Rule %s is not a valid child of Rule %s' % (
                child_rule.__name__, self.rule_name))
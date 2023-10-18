def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node."""
        for field_name in node._fields:
            setattr(node, field_name, self.visit(getattr(node, field_name)))
        return node
def visit(self, obj):
        """Visit a node or a list of nodes. Other values are ignored"""
        if isinstance(obj, list):
            return [self.visit(elt) for elt in obj]
        elif isinstance(obj, ast.AST):
            return self._visit_one(obj)
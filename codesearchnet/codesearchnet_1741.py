def visit(self, obj):
        """Visit a node or a list of nodes. Other values are ignored"""
        if isinstance(obj, list):
            return list(filter(lambda x: x is not None, map(self.visit, obj)))
        elif isinstance(obj, ast.AST):
            return self._visit_one(obj)
        else:
            return obj
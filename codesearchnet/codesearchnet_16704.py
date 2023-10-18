def _baseattrs(self):
        """A dict of members expressed in literals"""

        result = {
            "type": type(self).__name__,
            "obj": self.cells._baseattrs,
            "args": self.args,
            "value": self.value if self.has_value else None,
            "predslen": len(self.preds),
            "succslen": len(self.succs),
            "repr_parent": self.cells._impl.repr_parent(),
            "repr": self.cells._get_repr(),
        }

        return result
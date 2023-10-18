def _baseattrs(self):
        """A dict of members expressed in literals"""

        result = super()._baseattrs
        result["static_spaces"] = self.static_spaces._baseattrs
        result["dynamic_spaces"] = self.dynamic_spaces._baseattrs
        result["cells"] = self.cells._baseattrs
        result["refs"] = self.refs._baseattrs

        if self.has_params():
            result["params"] = ", ".join(self.parameters)
        else:
            result["params"] = ""

        return result
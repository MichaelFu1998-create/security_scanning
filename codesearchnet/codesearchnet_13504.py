def add_feature(self,var):
        """Add a feature to `self`.

        :Parameters:
            - `var`: the feature name.
        :Types:
            - `var`: `unicode`"""
        if self.has_feature(var):
            return
        n=self.xmlnode.newChild(None, "feature", None)
        n.setProp("var", to_utf8(var))
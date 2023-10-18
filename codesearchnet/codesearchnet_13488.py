def set_name(self, name):
        """Set the name of the item.

        :Parameters:
            - `name`: the new name or `None`.
        :Types:
            - `name`: `unicode` """
        if name is None:
            if self.xmlnode.hasProp("name"):
                self.xmlnode.unsetProp("name")
            return
        name = unicode(name)
        self.xmlnode.setProp("name", name.encode("utf-8"))
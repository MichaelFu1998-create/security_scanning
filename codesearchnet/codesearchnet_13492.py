def set_name(self,name):
        """Set the name of the item.

        :Parameters:
            - `name`: the new name or `None`.
        :Types:
            - `name`: `unicode` """
        if not name:
            raise ValueError("name is required in DiscoIdentity")
        name = unicode(name)
        self.xmlnode.setProp("name", name.encode("utf-8"))
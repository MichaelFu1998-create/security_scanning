def set_type(self, item_type):
        """Set the type of the item.

        :Parameters:
            - `item_type`: the new type.
        :Types:
            - `item_type`: `unicode` """
        if not item_type:
            raise ValueError("Type is required in DiscoIdentity")
        item_type = unicode(item_type)
        self.xmlnode.setProp("type", item_type.encode("utf-8"))
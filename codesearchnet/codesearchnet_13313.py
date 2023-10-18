def add_item(self,item):
        """Add an item to `self`.

        :Parameters:
            - `item`: the item to add.
        :Types:
            - `item`: `MucItemBase`
        """
        if not isinstance(item,MucItemBase):
            raise TypeError("Bad item type for muc#user")
        item.as_xml(self.xmlnode)
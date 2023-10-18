def get_type(self):
        """Get the type of the item.

        :return: the type of the item.
        :returntype: `unicode`"""
        item_type = self.xmlnode.prop("type")
        if not item_type:
            item_type = "?"
        return item_type.decode("utf-8")
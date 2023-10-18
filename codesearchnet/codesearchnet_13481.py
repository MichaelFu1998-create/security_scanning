def add_item(self, fields = None):
        """Add and item to the form.

        :Parameters:
            - `fields`: fields of the item (they may be added later).
        :Types:
            - `fields`: `list` of `Field`

        :return: the item added.
        :returntype: `Item`
        """
        item = Item(fields)
        self.items.append(item)
        return item
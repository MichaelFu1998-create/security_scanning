def set_category(self, category):
        """Set the category of the item.

        :Parameters:
            - `category`: the new category.
        :Types:
            - `category`: `unicode` """
        if not category:
            raise ValueError("Category is required in DiscoIdentity")
        category = unicode(category)
        self.xmlnode.setProp("category", category.encode("utf-8"))
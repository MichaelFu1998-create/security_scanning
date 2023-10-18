def get_category(self):
        """Get the category of the item.

        :return: the category of the item.
        :returntype: `unicode`"""
        var = self.xmlnode.prop("category")
        if not var:
            var = "?"
        return var.decode("utf-8")
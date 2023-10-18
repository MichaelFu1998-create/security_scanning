def get_name(self):
        """Get the name of the item.

        :return: the name of the item or `None`.
        :returntype: `unicode`"""
        var = self.xmlnode.prop("name")
        if not var:
            var = ""
        return var.decode("utf-8")
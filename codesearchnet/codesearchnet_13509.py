def add_identity(self,item_name,item_category=None,item_type=None):
        """Add an identity to the `DiscoInfo` object.

        :Parameters:
            - `item_name`: name of the item.
            - `item_category`: category of the item.
            - `item_type`: type of the item.
        :Types:
            - `item_name`: `unicode`
            - `item_category`: `unicode`
            - `item_type`: `unicode`

        :returns: the identity created.
        :returntype: `DiscoIdentity`"""
        return DiscoIdentity(self,item_name,item_category,item_type)
def add_item(self,jid,node=None,name=None,action=None):
        """Add a new item to the `DiscoItems` object.

        :Parameters:
            - `jid`: item JID.
            - `node`: item node name.
            - `name`: item name.
            - `action`: action for a "disco push".
        :Types:
            - `jid`: `pyxmpp.JID`
            - `node`: `unicode`
            - `name`: `unicode`
            - `action`: `unicode`

        :returns: the item created.
        :returntype: `DiscoItem`."""
        return DiscoItem(self,jid,node,name,action)
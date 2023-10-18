def set_items(self, item_list):
        """Set items in the disco#items object.

        All previous items are removed.

        :Parameters:
            - `item_list`: list of items or item properties
              (jid,node,name,action).
        :Types:
            - `item_list`: sequence of `DiscoItem` or sequence of sequences
        """
        for item in self.items:
            item.remove()
        for item in item_list:
            try:
                self.add_item(item.jid,item.node,item.name,item.action)
            except AttributeError:
                self.add_item(*item)
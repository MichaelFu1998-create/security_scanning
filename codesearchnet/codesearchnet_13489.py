def set_node(self,node):
        """Set the node of the item.

        :Parameters:
            - `node`: the new node or `None`.
        :Types:
            - `node`: `unicode`
        """
        if node is None:
            if self.xmlnode.hasProp("node"):
                self.xmlnode.unsetProp("node")
            return
        node = unicode(node)
        self.xmlnode.setProp("node", node.encode("utf-8"))
def deserialize_data(self, workflow, start_node):
        """
        Reads a "data" or "define" tag from the given node.

        start_node -- the xml node (xml.dom.minidom.Node)
        """
        name = start_node.getAttribute('name')
        value = start_node.getAttribute('value')
        return name, value
def deserialize_assign_list(self, workflow, start_node):
        """
        Reads a list of assignments from the given node.

        workflow -- the workflow
        start_node -- the xml structure (xml.dom.minidom.Node)
        """
        # Collect all information.
        assignments = []
        for node in start_node.childNodes:
            if node.nodeType != minidom.Node.ELEMENT_NODE:
                continue
            if node.nodeName.lower() == 'assign':
                assignments.append(self.deserialize_assign(workflow, node))
            else:
                _exc('Unknown node: %s' % node.nodeName)
        return assignments
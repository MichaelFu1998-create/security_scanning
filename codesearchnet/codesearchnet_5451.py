def deserialize_condition(self, workflow, start_node):
        """
        Reads the conditional statement from the given node.

        workflow -- the workflow with which the concurrence is associated
        start_node -- the xml structure (xml.dom.minidom.Node)
        """
        # Collect all information.
        condition = None
        spec_name = None
        for node in start_node.childNodes:
            if node.nodeType != minidom.Node.ELEMENT_NODE:
                continue
            if node.nodeName.lower() == 'successor':
                if spec_name is not None:
                    _exc('Duplicate task name %s' % spec_name)
                if node.firstChild is None:
                    _exc('Successor tag without a task name')
                spec_name = node.firstChild.nodeValue
            elif node.nodeName.lower() in _op_map:
                if condition is not None:
                    _exc('Multiple conditions are not yet supported')
                condition = self.deserialize_logical(node)
            else:
                _exc('Unknown node: %s' % node.nodeName)

        if condition is None:
            _exc('Missing condition in conditional statement')
        if spec_name is None:
            _exc('A %s has no task specified' % start_node.nodeName)
        return condition, spec_name
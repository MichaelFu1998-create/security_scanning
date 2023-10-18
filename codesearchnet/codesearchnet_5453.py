def deserialize_workflow_spec(self, s_state, filename=None):
        """
        Reads the workflow from the given XML structure and returns a
        WorkflowSpec instance.
        """
        dom = minidom.parseString(s_state)
        node = dom.getElementsByTagName('process-definition')[0]
        name = node.getAttribute('name')
        if name == '':
            _exc('%s without a name attribute' % node.nodeName)

        # Read all task specs and create a list of successors.
        workflow_spec = specs.WorkflowSpec(name, filename)
        del workflow_spec.task_specs['Start']
        end = specs.Simple(workflow_spec, 'End'), []
        read_specs = dict(end=end)
        for child_node in node.childNodes:
            if child_node.nodeType != minidom.Node.ELEMENT_NODE:
                continue
            if child_node.nodeName == 'name':
                workflow_spec.name = child_node.firstChild.nodeValue
            elif child_node.nodeName == 'description':
                workflow_spec.description = child_node.firstChild.nodeValue
            elif child_node.nodeName.lower() in _spec_map:
                self.deserialize_task_spec(
                    workflow_spec, child_node, read_specs)
            else:
                _exc('Unknown node: %s' % child_node.nodeName)

        # Remove the default start-task from the workflow.
        workflow_spec.start = read_specs['start'][0]

        # Connect all task specs.
        for name in read_specs:
            spec, successors = read_specs[name]
            for condition, successor_name in successors:
                if successor_name not in read_specs:
                    _exc('Unknown successor: "%s"' % successor_name)
                successor, foo = read_specs[successor_name]
                if condition is None:
                    spec.connect(successor)
                else:
                    spec.connect_if(condition, successor)
        return workflow_spec
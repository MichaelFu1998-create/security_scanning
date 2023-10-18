def deserialize_assign(self, workflow, start_node):
        """
        Reads the "pre-assign" or "post-assign" tag from the given node.

        start_node -- the xml node (xml.dom.minidom.Node)
        """
        name = start_node.getAttribute('name')
        attrib = start_node.getAttribute('field')
        value = start_node.getAttribute('value')
        kwargs = {}
        if name == '':
            _exc('name attribute required')
        if attrib != '' and value != '':
            _exc('Both, field and right-value attributes found')
        elif attrib == '' and value == '':
            _exc('field or value attribute required')
        elif value != '':
            kwargs['right'] = value
        else:
            kwargs['right_attribute'] = attrib
        return operators.Assign(name, **kwargs)
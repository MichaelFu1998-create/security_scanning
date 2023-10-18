def deserialize_logical(self, node):
        """
        Reads the logical tag from the given node, returns a Condition object.

        node -- the xml node (xml.dom.minidom.Node)
        """
        term1_attrib = node.getAttribute('left-field')
        term1_value = node.getAttribute('left-value')
        op = node.nodeName.lower()
        term2_attrib = node.getAttribute('right-field')
        term2_value = node.getAttribute('right-value')
        if op not in _op_map:
            _exc('Invalid operator')
        if term1_attrib != '' and term1_value != '':
            _exc('Both, left-field and left-value attributes found')
        elif term1_attrib == '' and term1_value == '':
            _exc('left-field or left-value attribute required')
        elif term1_value != '':
            left = term1_value
        else:
            left = operators.Attrib(term1_attrib)
        if term2_attrib != '' and term2_value != '':
            _exc('Both, right-field and right-value attributes found')
        elif term2_attrib == '' and term2_value == '':
            _exc('right-field or right-value attribute required')
        elif term2_value != '':
            right = term2_value
        else:
            right = operators.Attrib(term2_attrib)
        return _op_map[op](left, right)
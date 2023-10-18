def serialize_value_list(self, list_elem, thelist):
        """
        Serializes a list, where the values are objects of type
        str, Attrib, or PathAttrib.

        Example::

            <value>text</value>
            <value><attribute>foobar</attribute></value>
            <value><path>foobar</path></value>
        """
        for value in thelist:
            value_elem = SubElement(list_elem, 'value')
            self.serialize_value(value_elem, value)
        return list_elem
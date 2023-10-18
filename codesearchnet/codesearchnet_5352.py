def serialize_value_map(self, map_elem, thedict):
        """
        Serializes a dictionary of key/value pairs, where the values are
        either strings, or Attrib, or PathAttrib objects.

        Example::

            <variable>
                <name>foo</name>
                <value>text</value>
            </variable>
            <variable>
                <name>foo2</name>
                <value><attribute>foobar</attribute></value>
            </variable>
        """
        for key, value in sorted((str(k), v) for (k, v) in thedict.items()):
            var_elem = SubElement(map_elem, 'variable')
            SubElement(var_elem, 'name').text = str(key)
            value_elem = SubElement(var_elem, 'value')
            self.serialize_value(value_elem, value)
        return map_elem
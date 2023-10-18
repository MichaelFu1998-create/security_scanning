def serialize_value(self, parent_elem, value):
        """
        Serializes str, Attrib, or PathAttrib objects.

        Example::

            <attribute>foobar</attribute>
        """
        if isinstance(value, (str, int)) or type(value).__name__ == 'str':
            parent_elem.text = str(value)
        elif value is None:
            parent_elem.text = None
        else:
            parent_elem.append(value.serialize(self))
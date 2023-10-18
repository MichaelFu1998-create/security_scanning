def serialize_attrib(self, op):
        """
        Serializer for :meth:`SpiffWorkflow.operators.Attrib`.

        Example::

            <attribute>foobar</attribute>
        """
        elem = etree.Element('attribute')
        elem.text = op.name
        return elem
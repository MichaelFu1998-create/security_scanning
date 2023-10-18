def serialize_assign(self, op):
        """
        Serializer for :meth:`SpiffWorkflow.operators.Assign`.

        Example::

            <assign>
                <name>foobar</name>
                <value>doodle</value>
            </assign>
        """
        elem = etree.Element('assign')
        self.serialize_value(SubElement(elem, 'name'), op.left_attribute)
        if op.right:
            self.serialize_value(SubElement(elem, 'value'), op.right)
        if op.right_attribute:
            self.serialize_value(
                SubElement(elem, 'value-attribute'), op.right_attribute)
        return elem
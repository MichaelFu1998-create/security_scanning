def serialize_operator_equal(self, op):
        """
        Serializer for :meth:`SpiffWorkflow.operators.Equal`.

        Example::

            <equals>
                <value>text</value>
                <value><attribute>foobar</attribute></value>
                <value><path>foobar</path></value>
            </equals>
        """
        elem = etree.Element('equals')
        return self.serialize_value_list(elem, op.args)
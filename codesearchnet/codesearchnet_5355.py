def serialize_operator_not_equal(self, op):
        """
        Serializer for :meth:`SpiffWorkflow.operators.NotEqual`.

        Example::

            <not-equals>
                <value>text</value>
                <value><attribute>foobar</attribute></value>
                <value><path>foobar</path></value>
            </not-equals>
        """
        elem = etree.Element('not-equals')
        return self.serialize_value_list(elem, op.args)
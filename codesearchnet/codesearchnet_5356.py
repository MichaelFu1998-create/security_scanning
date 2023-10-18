def serialize_operator_greater_than(self, op):
        """
        Serializer for :meth:`SpiffWorkflow.operators.NotEqual`.

        Example::

            <greater-than>
                <value>text</value>
                <value><attribute>foobar</attribute></value>
            </greater-than>
        """
        elem = etree.Element('greater-than')
        return self.serialize_value_list(elem, op.args)
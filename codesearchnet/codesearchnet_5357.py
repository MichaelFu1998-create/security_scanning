def serialize_operator_less_than(self, op):
        """
        Serializer for :meth:`SpiffWorkflow.operators.NotEqual`.

        Example::

            <less-than>
                <value>text</value>
                <value><attribute>foobar</attribute></value>
            </less-than>
        """
        elem = etree.Element('less-than')
        return self.serialize_value_list(elem, op.args)
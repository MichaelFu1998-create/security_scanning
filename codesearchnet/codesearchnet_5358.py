def serialize_operator_match(self, op):
        """
        Serializer for :meth:`SpiffWorkflow.operators.NotEqual`.

        Example::

            <matches>
                <value>text</value>
                <value><attribute>foobar</attribute></value>
            </matches>
        """
        elem = etree.Element('matches')
        return self.serialize_value_list(elem, op.args)
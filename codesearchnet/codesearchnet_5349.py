def serialize_pathattrib(self, op):
        """
        Serializer for :meth:`SpiffWorkflow.operators.PathAttrib`.

        Example::

            <path>foobar</path>
        """
        elem = etree.Element('path')
        elem.text = op.path
        return elem
def serialize_acquire_mutex(self, spec):
        """
        Serializer for :meth:`SpiffWorkflow.specs.AcquireMutex`.
        """
        elem = etree.Element('acquire-mutex')
        self.serialize_task_spec(spec, elem)
        SubElement(elem, 'mutex').text = spec.mutex
        return elem
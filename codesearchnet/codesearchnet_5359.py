def serialize_task_spec(self, spec, elem):
        """
        Serializes common attributes of :meth:`SpiffWorkflow.specs.TaskSpec`.
        """
        if spec.id is not None:
            SubElement(elem, 'id').text = str(spec.id)
        SubElement(elem, 'name').text = spec.name
        if spec.description:
            SubElement(elem, 'description').text = spec.description
        if spec.manual:
            SubElement(elem, 'manual')
        if spec.internal:
            SubElement(elem, 'internal')
        SubElement(elem, 'lookahead').text = str(spec.lookahead)
        inputs = [t.name for t in spec.inputs]
        outputs = [t.name for t in spec.outputs]
        self.serialize_value_list(SubElement(elem, 'inputs'), inputs)
        self.serialize_value_list(SubElement(elem, 'outputs'), outputs)
        self.serialize_value_map(SubElement(elem, 'data'), spec.data)
        self.serialize_value_map(SubElement(elem, 'defines'), spec.defines)
        self.serialize_value_list(SubElement(elem, 'pre-assign'),
                                  spec.pre_assign)
        self.serialize_value_list(SubElement(elem, 'post-assign'),
                                  spec.post_assign)

        # Note: Events are not serialized; this is documented in
        # the TaskSpec API docs.

        return elem
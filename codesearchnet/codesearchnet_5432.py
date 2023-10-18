def _fix_call_activities_signavio(self, bpmn, filename):
        """
        Signavio produces slightly invalid BPMN for call activity nodes... It
        is supposed to put a reference to the id of the called process in to
        the calledElement attribute. Instead it stores a string (which is the
        name of the process - not its ID, in our interpretation) in an
        extension tag.

        This code gets the name of the 'subprocess reference', finds a process
        with a matching name, and sets the calledElement attribute to the id of
        the process.
        """
        for node in xpath_eval(bpmn)(".//bpmn:callActivity"):
            calledElement = node.get('calledElement', None)
            if not calledElement:
                signavioMetaData = xpath_eval(node, extra_ns={
                    'signavio': SIGNAVIO_NS})(
                    './/signavio:signavioMetaData[@metaKey="entry"]')
                if not signavioMetaData:
                    raise ValidationException(
                        'No Signavio "Subprocess reference" specified.',
                        node=node, filename=filename)
                subprocess_reference = one(signavioMetaData).get('metaValue')
                matches = []
                for b in list(self.bpmn.values()):
                    for p in xpath_eval(b)(".//bpmn:process"):
                        if (p.get('name', p.get('id', None)) ==
                                subprocess_reference):
                            matches.append(p)
                if not matches:
                    raise ValidationException(
                        "No matching process definition found for '%s'." %
                        subprocess_reference, node=node, filename=filename)
                if len(matches) != 1:
                    raise ValidationException(
                        "More than one matching process definition "
                        " found for '%s'." % subprocess_reference, node=node,
                        filename=filename)

                node.set('calledElement', matches[0].get('id'))
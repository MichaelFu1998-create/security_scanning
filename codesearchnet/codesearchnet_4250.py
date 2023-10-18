def add_annotator(self, doc, annotator):
        """Adds an annotator to the SPDX Document.
        Annotator is an entity created by an EntityBuilder.
        Raises SPDXValueError if not a valid annotator type.
        """
        # Each annotator marks the start of a new annotation object.
        # FIXME: this state does not make sense
        self.reset_annotations()
        if validations.validate_annotator(annotator):
            doc.add_annotation(annotation.Annotation(annotator=annotator))
            return True
        else:
            raise SPDXValueError('Annotation::Annotator')
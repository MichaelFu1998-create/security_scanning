def add_annotation_type(self, doc, annotation_type):
        """Sets the annotation type. Raises CardinalityError if
        already set. OrderError if no annotator defined before.
        Raises SPDXValueError if invalid value.
        """
        if len(doc.annotations) != 0:
            if not self.annotation_type_set:
                self.annotation_type_set = True
                if validations.validate_annotation_type(annotation_type):
                    doc.annotations[-1].annotation_type = annotation_type
                    return True
                else:
                    raise SPDXValueError('Annotation::AnnotationType')
            else:
                raise CardinalityError('Annotation::AnnotationType')
        else:
            raise OrderError('Annotation::AnnotationType')
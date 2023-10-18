def add_annotation_type(self, doc, annotation_type):
        """Sets the annotation type. Raises CardinalityError if
        already set. OrderError if no annotator defined before.
        """
        if len(doc.annotations) != 0:
            if not self.annotation_type_set:
                if annotation_type.endswith('annotationType_other'):
                    self.annotation_type_set = True
                    doc.annotations[-1].annotation_type = 'OTHER'
                    return True
                elif annotation_type.endswith('annotationType_review'):
                    self.annotation_type_set = True
                    doc.annotations[-1].annotation_type = 'REVIEW'
                    return True
                else:
                    raise SPDXValueError('Annotation::AnnotationType')
            else:
                raise CardinalityError('Annotation::AnnotationType')
        else:
            raise OrderError('Annotation::AnnotationType')
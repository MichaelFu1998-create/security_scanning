def add_annotation_date(self, doc, annotation_date):
        """Sets the annotation date. Raises CardinalityError if
        already set. OrderError if no annotator defined before.
        Raises SPDXValueError if invalid value.
        """
        if len(doc.annotations) != 0:
            if not self.annotation_date_set:
                self.annotation_date_set = True
                date = utils.datetime_from_iso_format(annotation_date)
                if date is not None:
                    doc.annotations[-1].annotation_date = date
                    return True
                else:
                    raise SPDXValueError('Annotation::AnnotationDate')
            else:
                raise CardinalityError('Annotation::AnnotationDate')
        else:
            raise OrderError('Annotation::AnnotationDate')
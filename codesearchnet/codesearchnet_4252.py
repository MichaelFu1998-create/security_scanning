def add_annotation_comment(self, doc, comment):
        """Sets the annotation comment. Raises CardinalityError if
        already set. OrderError if no annotator defined before.
        Raises SPDXValueError if comment is not free form text.
        """
        if len(doc.annotations) != 0:
            if not self.annotation_comment_set:
                self.annotation_comment_set = True
                if validations.validate_annotation_comment(comment):
                    doc.annotations[-1].comment = str_from_text(comment)
                    return True
                else:
                    raise SPDXValueError('AnnotationComment::Comment')
            else:
                raise CardinalityError('AnnotationComment::Comment')
        else:
            raise OrderError('AnnotationComment::Comment')
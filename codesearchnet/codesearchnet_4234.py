def set_doc_comment(self, doc, comment):
        """Sets document comment, Raises CardinalityError if
        comment already set.
        Raises SPDXValueError if comment is not free form text.
        """
        if not self.doc_comment_set:
            self.doc_comment_set = True
            if validations.validate_doc_comment(comment):
                doc.comment = str_from_text(comment)
                return True
            else:
                raise SPDXValueError('Document::Comment')
        else:
            raise CardinalityError('Document::Comment')
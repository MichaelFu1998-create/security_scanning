def add_review_comment(self, doc, comment):
        """Sets the review comment. Raises CardinalityError if
        already set. OrderError if no reviewer defined before.
        Raises SPDXValueError if comment is not free form text.
        """
        if len(doc.reviews) != 0:
            if not self.review_comment_set:
                self.review_comment_set = True
                if validations.validate_review_comment(comment):
                    doc.reviews[-1].comment = str_from_text(comment)
                    return True
                else:
                    raise SPDXValueError('ReviewComment::Comment')
            else:
                raise CardinalityError('ReviewComment')
        else:
            raise OrderError('ReviewComment')
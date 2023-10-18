def add_reviewer(self, doc, reviewer):
        """Adds a reviewer to the SPDX Document.
        Reviwer is an entity created by an EntityBuilder.
        Raises SPDXValueError if not a valid reviewer type.
        """
        # Each reviewer marks the start of a new review object.
        # FIXME: this state does not make sense
        self.reset_reviews()
        if validations.validate_reviewer(reviewer):
            doc.add_review(review.Review(reviewer=reviewer))
            return True
        else:
            raise SPDXValueError('Review::Reviewer')
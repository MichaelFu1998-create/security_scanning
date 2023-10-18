def add_review_date(self, doc, reviewed):
        """Sets the review date. Raises CardinalityError if
        already set. OrderError if no reviewer defined before.
        Raises SPDXValueError if invalid reviewed value.
        """
        if len(doc.reviews) != 0:
            if not self.review_date_set:
                self.review_date_set = True
                date = utils.datetime_from_iso_format(reviewed)
                if date is not None:
                    doc.reviews[-1].review_date = date
                    return True
                else:
                    raise SPDXValueError('Review::ReviewDate')
            else:
                raise CardinalityError('Review::ReviewDate')
        else:
            raise OrderError('Review::ReviewDate')
def set_lic_comment(self, doc, comment):
        """Sets license comment.
        Raises SPDXValueError if comment is not free form text.
        Raises OrderError if no license ID defined.
        """
        if self.has_extr_lic(doc):
            if not self.extr_lic_comment_set:
                self.extr_lic_comment_set = True
                if validations.validate_is_free_form_text(comment):
                    self.extr_lic(doc).comment = str_from_text(comment)
                    return True
                else:
                    raise SPDXValueError('ExtractedLicense::comment')
            else:
                raise CardinalityError('ExtractedLicense::comment')
        else:
            raise OrderError('ExtractedLicense::comment')
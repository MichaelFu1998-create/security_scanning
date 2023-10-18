def set_lic_text(self, doc, text):
        """Sets license extracted text.
        Raises SPDXValueError if text is not free form text.
        Raises OrderError if no license ID defined.
        """
        if self.has_extr_lic(doc):
            if not self.extr_text_set:
                self.extr_text_set = True
                if validations.validate_is_free_form_text(text):
                    self.extr_lic(doc).text = str_from_text(text)
                    return True
                else:
                    raise SPDXValueError('ExtractedLicense::text')
            else:
                raise CardinalityError('ExtractedLicense::text')
        else:
            raise OrderError('ExtractedLicense::text')
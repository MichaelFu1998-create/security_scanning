def get_extr_license_text(self, extr_lic):
        """
        Return extracted text  from an ExtractedLicense or None.
        """
        text_tripples = list(self.graph.triples((extr_lic, self.spdx_namespace['extractedText'], None)))
        if not text_tripples:
            self.error = True
            msg = 'Extracted license must have extractedText property'
            self.logger.log(msg)
            return

        if len(text_tripples) > 1:
            self.more_than_one_error('extracted license text')
            return

        text_tripple = text_tripples[0]
        _s, _p, text = text_tripple
        return text
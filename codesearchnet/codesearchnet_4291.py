def add_lic_xref(self, doc, ref):
        """Adds a license cross reference.
        Raises OrderError if no License ID defined.
        """
        if self.has_extr_lic(doc):
            self.extr_lic(doc).add_xref(ref)
            return True
        else:
            raise OrderError('ExtractedLicense::CrossRef')
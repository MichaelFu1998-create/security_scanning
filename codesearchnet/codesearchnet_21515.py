def is_draft(self):
        """Document is a draft if ``'lsstdoc'`` is included in the
        documentclass options (`bool`).
        """
        if not hasattr(self, '_document_options'):
            self._parse_documentclass()

        if 'lsstdraft' in self._document_options:
            return True
        else:
            return False
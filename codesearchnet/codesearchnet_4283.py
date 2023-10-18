def add_file_contribution(self, doc, value):
        """Raises OrderError if no package or file defined.
        """
        if self.has_package(doc) and self.has_file(doc):
            self.file(doc).add_contrib(value)
        else:
            raise OrderError('File::Contributor')
def add_file_dep(self, doc, value):
        """Raises OrderError if no package or file defined.
        """
        if self.has_package(doc) and self.has_file(doc):
            self.file(doc).add_depend(value)
        else:
            raise OrderError('File::Dependency')
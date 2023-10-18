def set_file_atrificat_of_project(self, doc, symbol, value):
        """Sets a file name, uri or home artificat.
        Raises OrderError if no package or file defined.
        """
        if self.has_package(doc) and self.has_file(doc):
            self.file(doc).add_artifact(symbol, value)
        else:
            raise OrderError('File::Artificat')
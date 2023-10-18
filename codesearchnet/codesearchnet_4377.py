def set_file_copyright(self, doc, text):
        """Raises OrderError if no package or file defined.
        Raises CardinalityError if more than one.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_copytext_set:
                self.file_copytext_set = True
                self.file(doc).copyright = text
                return True
            else:
                raise CardinalityError('File::CopyRight')
        else:
            raise OrderError('File::CopyRight')
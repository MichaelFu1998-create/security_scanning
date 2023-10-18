def set_file_comment(self, doc, text):
        """Raises OrderError if no package or no file defined.
        Raises CardinalityError if more than one comment set.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_comment_set:
                self.file_comment_set = True
                self.file(doc).comment = text
                return True
            else:
                raise CardinalityError('File::Comment')
        else:
            raise OrderError('File::Comment')
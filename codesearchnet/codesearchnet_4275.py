def set_file_comment(self, doc, text):
        """
        Raises OrderError if no package or no file defined.
        Raises CardinalityError if more than one comment set.
        Raises SPDXValueError if text is not free form text.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_comment_set:
                self.file_comment_set = True
                if validations.validate_file_comment(text):
                    self.file(doc).comment = str_from_text(text)
                    return True
                else:
                    raise SPDXValueError('File::Comment')
            else:
                raise CardinalityError('File::Comment')
        else:
            raise OrderError('File::Comment')
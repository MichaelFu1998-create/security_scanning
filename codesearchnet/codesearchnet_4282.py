def set_file_notice(self, doc, text):
        """Raises OrderError if no package or file defined.
        Raises SPDXValueError if not free form text.
        Raises CardinalityError if more than one.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_notice_set:
                self.file_notice_set = True
                if validations.validate_file_notice(text):
                    self.file(doc).notice = str_from_text(text)
                else:
                    raise SPDXValueError('File::Notice')
            else:
                raise CardinalityError('File::Notice')
        else:
            raise OrderError('File::Notice')
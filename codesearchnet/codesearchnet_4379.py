def set_file_notice(self, doc, text):
        """Raises OrderError if no package or file defined.
        Raises CardinalityError if more than one.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_notice_set:
                self.file_notice_set = True
                self.file(doc).notice = tagvaluebuilders.str_from_text(text)
                return True
            else:
                raise CardinalityError('File::Notice')
        else:
            raise OrderError('File::Notice')
def set_file_copyright(self, doc, text):
        """Raises OrderError if no package or file defined.
        Raises SPDXValueError if not free form text or NONE or NO_ASSERT.
        Raises CardinalityError if more than one.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_copytext_set:
                self.file_copytext_set = True
                if validations.validate_file_cpyright(text):
                    if isinstance(text, string_types):
                        self.file(doc).copyright = str_from_text(text)
                    else:
                        self.file(doc).copyright = text  # None or NoAssert
                    return True
                else:
                    raise SPDXValueError('File::CopyRight')
            else:
                raise CardinalityError('File::CopyRight')
        else:
            raise OrderError('File::CopyRight')
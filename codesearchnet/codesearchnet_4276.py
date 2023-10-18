def set_file_type(self, doc, type_value):
        """
        Raises OrderError if no package or file defined.
        Raises CardinalityError if more than one type set.
        Raises SPDXValueError if type is unknown.
        """
        type_dict = {
            'SOURCE': file.FileType.SOURCE,
            'BINARY': file.FileType.BINARY,
            'ARCHIVE': file.FileType.ARCHIVE,
            'OTHER': file.FileType.OTHER
        }
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_type_set:
                self.file_type_set = True
                if type_value in type_dict.keys():
                    self.file(doc).type = type_dict[type_value]
                    return True
                else:
                    raise SPDXValueError('File::Type')
            else:
                raise CardinalityError('File::Type')
        else:
            raise OrderError('File::Type')
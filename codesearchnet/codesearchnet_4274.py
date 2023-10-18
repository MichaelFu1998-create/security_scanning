def set_file_spdx_id(self, doc, spdx_id):
        """
        Sets the file SPDX Identifier.
        Raises OrderError if no package or no file defined.
        Raises SPDXValueError if malformed value.
        Raises CardinalityError if more than one spdx_id set.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_spdx_id_set:
                self.file_spdx_id_set = True
                if validations.validate_file_spdx_id(spdx_id):
                    self.file(doc).spdx_id = spdx_id
                    return True
                else:
                    raise SPDXValueError('File::SPDXID')
            else:
                raise CardinalityError('File::SPDXID')
        else:
            raise OrderError('File::SPDXID')
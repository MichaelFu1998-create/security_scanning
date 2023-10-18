def set_file_chksum(self, doc, chksum):
        """
        Raises OrderError if no package or file defined.
        Raises CardinalityError if more than one chksum set.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_chksum_set:
                self.file_chksum_set = True
                self.file(doc).chk_sum = checksum_from_sha1(chksum)
                return True
            else:
                raise CardinalityError('File::CheckSum')
        else:
            raise OrderError('File::CheckSum')
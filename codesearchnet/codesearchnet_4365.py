def set_chksum(self, doc, chk_sum):
        """
        Sets the external document reference's check sum, if not already set.
        chk_sum - The checksum value in the form of a string.
        """
        if chk_sum:
            doc.ext_document_references[-1].check_sum = checksum.Algorithm(
                'SHA1', chk_sum)
        else:
            raise SPDXValueError('ExternalDocumentRef::Checksum')
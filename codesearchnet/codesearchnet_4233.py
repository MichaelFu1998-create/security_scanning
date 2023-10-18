def set_doc_spdx_id(self, doc, doc_spdx_id_line):
        """Sets the document SPDX Identifier.
        Raises value error if malformed value, CardinalityError
        if already defined.
        """
        if not self.doc_spdx_id_set:
            if doc_spdx_id_line == 'SPDXRef-DOCUMENT':
                doc.spdx_id = doc_spdx_id_line
                self.doc_spdx_id_set = True
                return True
            else:
                raise SPDXValueError('Document::SPDXID')
        else:
            raise CardinalityError('Document::SPDXID')
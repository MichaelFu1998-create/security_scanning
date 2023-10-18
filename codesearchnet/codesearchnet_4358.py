def parse_ext_doc_ref(self, ext_doc_ref_term):
        """
        Parses the External Document ID, SPDX Document URI and Checksum.
        """
        for _s, _p, o in self.graph.triples(
                (ext_doc_ref_term,
                 self.spdx_namespace['externalDocumentId'],
                 None)):
            try:
                self.builder.set_ext_doc_id(self.doc, six.text_type(o))
            except SPDXValueError:
                self.value_error('EXT_DOC_REF_VALUE', 'External Document ID')
                break

        for _s, _p, o in self.graph.triples(
                (ext_doc_ref_term,
                 self.spdx_namespace['spdxDocument'],
                 None)):
            try:
                self.builder.set_spdx_doc_uri(self.doc, six.text_type(o))
            except SPDXValueError:
                self.value_error('EXT_DOC_REF_VALUE', 'SPDX Document URI')
                break

        for _s, _p, checksum in self.graph.triples(
                (ext_doc_ref_term, self.spdx_namespace['checksum'], None)):
            for _, _, value in self.graph.triples(
                    (checksum, self.spdx_namespace['checksumValue'], None)):
                try:
                    self.builder.set_chksum(self.doc, six.text_type(value))
                except SPDXValueError:
                    self.value_error('EXT_DOC_REF_VALUE', 'Checksum')
                    break
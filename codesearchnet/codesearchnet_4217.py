def p_ext_doc_refs_1(self, p):
        """ext_doc_ref : EXT_DOC_REF DOC_REF_ID DOC_URI EXT_DOC_REF_CHKSUM"""
        try:
            if six.PY2:
                doc_ref_id = p[2].decode(encoding='utf-8')
                doc_uri = p[3].decode(encoding='utf-8')
                ext_doc_chksum = p[4].decode(encoding='utf-8')
            else:
                doc_ref_id = p[2]
                doc_uri = p[3]
                ext_doc_chksum = p[4]

            self.builder.add_ext_doc_refs(self.document, doc_ref_id, doc_uri,
                                          ext_doc_chksum)
        except SPDXValueError:
            self.error = True
            msg = ERROR_MESSAGES['EXT_DOC_REF_VALUE'].format(p.lineno(2))
            self.logger.log(msg)
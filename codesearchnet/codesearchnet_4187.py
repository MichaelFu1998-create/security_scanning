def p_spdx_id(self, p):
        """spdx_id : SPDX_ID LINE"""
        if six.PY2:
            value = p[2].decode(encoding='utf-8')
        else:
            value = p[2]
        if not self.builder.doc_spdx_id_set:
            self.builder.set_doc_spdx_id(self.document, value)
        else:
            self.builder.set_file_spdx_id(self.document, value)
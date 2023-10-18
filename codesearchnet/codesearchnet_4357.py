def parse_doc_fields(self, doc_term):
        """Parses the version, data license, name, SPDX Identifier, namespace,
        and comment."""
        try:
            self.builder.set_doc_spdx_id(self.doc, doc_term)
        except SPDXValueError:
            self.value_error('DOC_SPDX_ID_VALUE', doc_term)
        try:
            if doc_term.count('#', 0, len(doc_term)) <= 1:
                doc_namespace = doc_term.split('#')[0]
                self.builder.set_doc_namespace(self.doc, doc_namespace)
            else:
                self.value_error('DOC_NAMESPACE_VALUE', doc_term)
        except SPDXValueError:
            self.value_error('DOC_NAMESPACE_VALUE', doc_term)
        for _s, _p, o in self.graph.triples((doc_term, self.spdx_namespace['specVersion'], None)):
            try:
                self.builder.set_doc_version(self.doc, six.text_type(o))
            except SPDXValueError:
                self.value_error('DOC_VERS_VALUE', o)
            except CardinalityError:
                self.more_than_one_error('specVersion')
                break
        for _s, _p, o in self.graph.triples((doc_term, self.spdx_namespace['dataLicense'], None)):
            try:
                self.builder.set_doc_data_lic(self.doc, six.text_type(o))
            except SPDXValueError:
                self.value_error('DOC_D_LICS', o)
            except CardinalityError:
                self.more_than_one_error('dataLicense')
                break
        for _s, _p, o in self.graph.triples(
                (doc_term, self.spdx_namespace['name'], None)):
            try:
                self.builder.set_doc_name(self.doc, six.text_type(o))
            except CardinalityError:
                self.more_than_one_error('name')
                break
        for _s, _p, o in self.graph.triples((doc_term, RDFS.comment, None)):
            try:
                self.builder.set_doc_comment(self.doc, six.text_type(o))
            except CardinalityError:
                self.more_than_one_error('Document comment')
                break
def create_external_document_ref_node(self, ext_document_references):
        """
        Add and return a creation info node to graph
        """
        ext_doc_ref_node = BNode()
        type_triple = (ext_doc_ref_node, RDF.type, self.spdx_namespace.ExternalDocumentRef)
        self.graph.add(type_triple)

        ext_doc_id = Literal(
            ext_document_references.external_document_id)
        ext_doc_id_triple = (
            ext_doc_ref_node, self.spdx_namespace.externalDocumentId, ext_doc_id)
        self.graph.add(ext_doc_id_triple)

        doc_uri = Literal(
            ext_document_references.spdx_document_uri)
        doc_uri_triple = (
            ext_doc_ref_node, self.spdx_namespace.spdxDocument, doc_uri)
        self.graph.add(doc_uri_triple)

        checksum_node = self.create_checksum_node(
            ext_document_references.check_sum)
        self.graph.add(
            (ext_doc_ref_node, self.spdx_namespace.checksum, checksum_node))

        return ext_doc_ref_node
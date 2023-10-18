def create_doc(self):
        """
        Add and return the root document node to graph.
        """
        doc_node = URIRef('http://www.spdx.org/tools#SPDXRef-DOCUMENT')
        # Doc type
        self.graph.add((doc_node, RDF.type, self.spdx_namespace.SpdxDocument))
        # Version
        vers_literal = Literal(str(self.document.version))
        self.graph.add((doc_node, self.spdx_namespace.specVersion, vers_literal))
        # Data license
        data_lics = URIRef(self.document.data_license.url)
        self.graph.add((doc_node, self.spdx_namespace.dataLicense, data_lics))
        doc_name = URIRef(self.document.name)
        self.graph.add((doc_node, self.spdx_namespace.name, doc_name))
        return doc_node
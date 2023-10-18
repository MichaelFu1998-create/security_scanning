def create_extracted_license(self, lic):
        """
        Handle extracted license.
        Return the license node.
        """
        licenses = list(self.graph.triples((None, self.spdx_namespace.licenseId, lic.identifier)))
        if len(licenses) != 0:
            return licenses[0][0]  # return subject in first triple
        else:
            license_node = BNode()
            type_triple = (license_node, RDF.type, self.spdx_namespace.ExtractedLicensingInfo)
            self.graph.add(type_triple)
            ident_triple = (license_node, self.spdx_namespace.licenseId, Literal(lic.identifier))
            self.graph.add(ident_triple)
            text_triple = (license_node, self.spdx_namespace.extractedText, Literal(lic.text))
            self.graph.add(text_triple)
            if lic.full_name is not None:
                name_triple = (license_node, self.spdx_namespace.licenseName, self.to_special_value(lic.full_name))
                self.graph.add(name_triple)
            for ref in lic.cross_ref:
                triple = (license_node, RDFS.seeAlso, URIRef(ref))
                self.graph.add(triple)
            if lic.comment is not None:
                comment_triple = (license_node, RDFS.comment, Literal(lic.comment))
                self.graph.add(comment_triple)
            return license_node
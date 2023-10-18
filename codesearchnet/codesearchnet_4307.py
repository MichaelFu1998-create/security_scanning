def create_file_node(self, doc_file):
        """
        Create a node for spdx.file.
        """
        file_node = URIRef('http://www.spdx.org/files#{id}'.format(
            id=str(doc_file.spdx_id)))
        type_triple = (file_node, RDF.type, self.spdx_namespace.File)
        self.graph.add(type_triple)

        name_triple = (file_node, self.spdx_namespace.fileName, Literal(doc_file.name))
        self.graph.add(name_triple)

        if doc_file.has_optional_field('comment'):
            comment_triple = (file_node, RDFS.comment, Literal(doc_file.comment))
            self.graph.add(comment_triple)

        if doc_file.has_optional_field('type'):
            ftype = self.spdx_namespace[self.FILE_TYPES[doc_file.type]]
            ftype_triple = (file_node, self.spdx_namespace.fileType, ftype)
            self.graph.add(ftype_triple)

        self.graph.add((file_node, self.spdx_namespace.checksum, self.create_checksum_node(doc_file.chk_sum)))

        conc_lic_node = self.license_or_special(doc_file.conc_lics)
        conc_lic_triple = (file_node, self.spdx_namespace.licenseConcluded, conc_lic_node)
        self.graph.add(conc_lic_triple)

        license_info_nodes = map(self.license_or_special, doc_file.licenses_in_file)
        for lic in license_info_nodes:
            triple = (file_node, self.spdx_namespace.licenseInfoInFile, lic)
            self.graph.add(triple)

        if doc_file.has_optional_field('license_comment'):
            comment_triple = (file_node, self.spdx_namespace.licenseComments, Literal(doc_file.license_comment))
            self.graph.add(comment_triple)

        cr_text_node = self.to_special_value(doc_file.copyright)
        cr_text_triple = (file_node, self.spdx_namespace.copyrightText, cr_text_node)
        self.graph.add(cr_text_triple)

        if doc_file.has_optional_field('notice'):
            notice_triple = (file_node, self.spdx_namespace.noticeText, doc_file.notice)
            self.graph.add(notice_triple)

        contrib_nodes = map(lambda c: Literal(c), doc_file.contributors)
        contrib_triples = [(file_node, self.spdx_namespace.fileContributor, node) for node in contrib_nodes]
        for triple in contrib_triples:
            self.graph.add(triple)

        return file_node
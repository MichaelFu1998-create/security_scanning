def create_creation_info(self):
        """
        Add and return a creation info node to graph
        """
        ci_node = BNode()
        # Type property
        type_triple = (ci_node, RDF.type, self.spdx_namespace.CreationInfo)
        self.graph.add(type_triple)

        created_date = Literal(self.document.creation_info.created_iso_format)
        created_triple = (ci_node, self.spdx_namespace.created, created_date)
        self.graph.add(created_triple)

        creators = self.creators()
        for creator in creators:
            self.graph.add((ci_node, self.spdx_namespace.creator, creator))

        if self.document.creation_info.has_comment:
            comment_node = Literal(self.document.creation_info.comment)
            comment_triple = (ci_node, RDFS.comment, comment_node)
            self.graph.add(comment_triple)

        return ci_node
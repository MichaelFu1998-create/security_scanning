def create_disjunction_node(self, disjunction):
        """
        Return a node representing a disjunction of licenses.
        """
        node = BNode()
        type_triple = (node, RDF.type, self.spdx_namespace.DisjunctiveLicenseSet)
        self.graph.add(type_triple)
        licenses = self.licenses_from_tree(disjunction)
        for lic in licenses:
            member_triple = (node, self.spdx_namespace.member, lic)
            self.graph.add(member_triple)
        return node
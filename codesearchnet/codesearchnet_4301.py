def create_conjunction_node(self, conjunction):
        """
        Return a node representing a conjunction of licenses.
        """
        node = BNode()
        type_triple = (node, RDF.type, self.spdx_namespace.ConjunctiveLicenseSet)
        self.graph.add(type_triple)
        licenses = self.licenses_from_tree(conjunction)
        for lic in licenses:
            member_triple = (node, self.spdx_namespace.member, lic)
            self.graph.add(member_triple)
        return node
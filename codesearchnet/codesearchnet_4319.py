def handle_package_has_file(self, package, package_node):
        """
        Add hasFile triples to graph.
        Must be called after files have been added.
        """
        file_nodes = map(self.handle_package_has_file_helper, package.files)
        triples = [(package_node, self.spdx_namespace.hasFile, node) for node in file_nodes]
        for triple in triples:
            self.graph.add(triple)
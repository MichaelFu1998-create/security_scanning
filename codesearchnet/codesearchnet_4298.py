def create_checksum_node(self, chksum):
        """
        Return a node representing spdx.checksum.
        """
        chksum_node = BNode()
        type_triple = (chksum_node, RDF.type, self.spdx_namespace.Checksum)
        self.graph.add(type_triple)
        algorithm_triple = (chksum_node, self.spdx_namespace.algorithm, Literal(chksum.identifier))
        self.graph.add(algorithm_triple)
        value_triple = (chksum_node, self.spdx_namespace.checksumValue, Literal(chksum.value))
        self.graph.add(value_triple)
        return chksum_node
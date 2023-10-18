def package_verif_node(self, package):
        """
        Return a node representing package verification code.
        """
        verif_node = BNode()
        type_triple = (verif_node, RDF.type, self.spdx_namespace.PackageVerificationCode)
        self.graph.add(type_triple)
        value_triple = (verif_node, self.spdx_namespace.packageVerificationCodeValue, Literal(package.verif_code))
        self.graph.add(value_triple)
        excl_file_nodes = map(
            lambda excl: Literal(excl), package.verif_exc_files)
        excl_predicate = self.spdx_namespace.packageVerificationCodeExcludedFile
        excl_file_triples = [(verif_node, excl_predicate, xcl_file) for xcl_file in excl_file_nodes]
        for trp in excl_file_triples:
            self.graph.add(trp)
        return verif_node
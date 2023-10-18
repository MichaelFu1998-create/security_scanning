def handle_package_has_file_helper(self, pkg_file):
        """
        Return node representing pkg_file
        pkg_file should be instance of spdx.file.
        """
        nodes = list(self.graph.triples((None, self.spdx_namespace.fileName, Literal(pkg_file.name))))
        if len(nodes) == 1:
            return nodes[0][0]
        else:
            raise InvalidDocumentError('handle_package_has_file_helper could not' +
                                       ' find file node for file: {0}'.format(pkg_file.name))
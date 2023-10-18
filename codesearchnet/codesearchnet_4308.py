def add_file_dependencies_helper(self, doc_file):
        """
        Handle dependencies for a single file.
        - doc_file - instance of spdx.file.File.
        """
        subj_triples = list(self.graph.triples((None, self.spdx_namespace.fileName, Literal(doc_file.name))))
        if len(subj_triples) != 1:
            raise InvalidDocumentError('Could not find dependency subject {0}'.format(doc_file.name))
        subject_node = subj_triples[0][0]
        for dependency in doc_file.dependencies:
            dep_triples = list(self.graph.triples((None, self.spdx_namespace.fileName, Literal(dependency))))
            if len(dep_triples) == 1:
                dep_node = dep_triples[0][0]
                dep_triple = (subject_node, self.spdx_namespace.fileDependency, dep_node)
                self.graph.add(dep_triple)
            else:
                print('Warning could not resolve file dependency {0} -> {1}'.format(doc_file.name, dependency))
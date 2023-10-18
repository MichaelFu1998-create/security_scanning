def p_file_artifact(self, f_term, predicate):
        """Handles file artifactOf.
        Note: does not handle artifact of project URI.
        """
        for _, _, project in self.graph.triples((f_term, predicate, None)):
            if (project, RDF.type, self.doap_namespace['Project']):
                self.p_file_project(project)
            else:
                self.error = True
                msg = 'File must be artifact of doap:Project'
                self.logger.log(msg)
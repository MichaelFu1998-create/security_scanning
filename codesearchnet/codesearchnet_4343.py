def p_file_project(self, project):
        """Helper function for parsing doap:project name and homepage.
        and setting them using the file builder.
        """
        for _, _, name in self.graph.triples((project, self.doap_namespace['name'], None)):
            self.builder.set_file_atrificat_of_project(self.doc, 'name', six.text_type(name))
        for _, _, homepage in self.graph.triples(
            (project, self.doap_namespace['homepage'], None)):
            self.builder.set_file_atrificat_of_project(self.doc, 'home', six.text_type(homepage))
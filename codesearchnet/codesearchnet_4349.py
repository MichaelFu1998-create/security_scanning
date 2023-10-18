def p_file_lic_conc(self, f_term, predicate):
        """Sets file licenses concluded."""
        try:
            for _, _, licenses in self.graph.triples((f_term, predicate, None)):
                if (licenses, RDF.type, self.spdx_namespace['ConjunctiveLicenseSet']) in self.graph:
                    lics = self.handle_conjunctive_list(licenses)
                    self.builder.set_concluded_license(self.doc, lics)

                elif (licenses, RDF.type, self.spdx_namespace['DisjunctiveLicenseSet']) in self.graph:
                    lics = self.handle_disjunctive_list(licenses)
                    self.builder.set_concluded_license(self.doc, lics)

                else:
                    try:
                        lics = self.handle_lics(licenses)
                        self.builder.set_concluded_license(self.doc, lics)
                    except SPDXValueError:
                        self.value_error('FILE_SINGLE_LICS', licenses)
        except CardinalityError:
            self.more_than_one_error('file {0}'.format(predicate))
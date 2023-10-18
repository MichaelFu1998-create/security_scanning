def handle_pkg_lic(self, p_term, predicate, builder_func):
        """Handles package lics concluded or declared."""
        try:
            for _, _, licenses in self.graph.triples((p_term, predicate, None)):
                if (licenses, RDF.type, self.spdx_namespace['ConjunctiveLicenseSet']) in self.graph:
                    lics = self.handle_conjunctive_list(licenses)
                    builder_func(self.doc, lics)

                elif (licenses, RDF.type, self.spdx_namespace['DisjunctiveLicenseSet']) in self.graph:
                    lics = self.handle_disjunctive_list(licenses)
                    builder_func(self.doc, lics)

                else:
                    try:
                        lics = self.handle_lics(licenses)
                        builder_func(self.doc, lics)
                    except SPDXValueError:
                        self.value_error('PKG_SINGLE_LICS', licenses)
        except CardinalityError:
            self.more_than_one_error('package {0}'.format(predicate))
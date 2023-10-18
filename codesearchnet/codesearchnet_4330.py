def get_extr_lics_xref(self, extr_lic):
        """
        Return a list of cross references.
        """
        xrefs = list(self.graph.triples((extr_lic, RDFS.seeAlso, None)))
        return map(lambda xref_triple: xref_triple[2], xrefs)
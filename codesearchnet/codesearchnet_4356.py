def parse_creation_info(self, ci_term):
        """
        Parse creators, created and comment.
        """
        for _s, _p, o in self.graph.triples((ci_term, self.spdx_namespace['creator'], None)):
            try:
                ent = self.builder.create_entity(self.doc, six.text_type(o))
                self.builder.add_creator(self.doc, ent)
            except SPDXValueError:
                self.value_error('CREATOR_VALUE', o)

        for _s, _p, o in self.graph.triples((ci_term, self.spdx_namespace['created'], None)):
            try:
                self.builder.set_created_date(self.doc, six.text_type(o))
            except SPDXValueError:
                self.value_error('CREATED_VALUE', o)
            except CardinalityError:
                self.more_than_one_error('created')
                break

        for _s, _p, o in self.graph.triples((ci_term, RDFS.comment, None)):
            try:
                self.builder.set_creation_comment(self.doc, six.text_type(o))
            except CardinalityError:
                self.more_than_one_error('CreationInfo comment')
                break
        for _s, _p, o in self.graph.triples((ci_term, self.spdx_namespace['licenseListVersion'], None)):
            try:
                self.builder.set_lics_list_ver(self.doc, six.text_type(o))
            except CardinalityError:
                self.more_than_one_error('licenseListVersion')
                break
            except SPDXValueError:
                self.value_error('LL_VALUE', o)
def parse(self, fil):
        """Parses a file and returns a document object.
        File, a file like object.
        """
        self.error = False
        self.graph = Graph()
        self.graph.parse(file=fil, format='xml')
        self.doc = document.Document()

        for s, _p, o in self.graph.triples((None, RDF.type, self.spdx_namespace['SpdxDocument'])):
            self.parse_doc_fields(s)

        for s, _p, o in self.graph.triples((None, RDF.type, self.spdx_namespace['ExternalDocumentRef'])):
            self.parse_ext_doc_ref(s)

        for s, _p, o in self.graph.triples((None, RDF.type, self.spdx_namespace['CreationInfo'])):
            self.parse_creation_info(s)

        for s, _p, o in self.graph.triples((None, RDF.type, self.spdx_namespace['Package'])):
            self.parse_package(s)

        for s, _p, o in self.graph.triples((None, self.spdx_namespace['referencesFile'], None)):
            self.parse_file(o)

        for s, _p, o in self.graph.triples((None, self.spdx_namespace['reviewed'], None)):
            self.parse_review(o)

        for s, _p, o in self.graph.triples((None, self.spdx_namespace['annotation'], None)):
            self.parse_annotation(o)

        validation_messages = []
        # Report extra errors if self.error is False otherwise there will be
        # redundent messages
        validation_messages = self.doc.validate(validation_messages)
        if not self.error:
            if validation_messages:
                for msg in validation_messages:
                    self.logger.log(msg)
                self.error = True
        return self.doc, self.error
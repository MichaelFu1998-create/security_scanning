def init(self):
        """Create an Elasticsearch index if necessary
        """
        # ignore 400 (IndexAlreadyExistsException) when creating an index
        self.es.indices.create(index=self.params['index'], ignore=400)
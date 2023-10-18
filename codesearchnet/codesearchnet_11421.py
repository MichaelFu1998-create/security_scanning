def _get_mappings(self, doc_type):
        """
        Interfaces with the elasticsearch mappings for the index
        prevents multiple loading of the same mappings from ES when called more than once

        Mappings format in elasticsearch is as follows:
        {
           "doc_type": {
              "properties": {
                 "nested_property": {
                    "properties": {
                       "an_analysed_property": {
                          "type": "string"
                       },
                       "another_analysed_property": {
                          "type": "string"
                       }
                    }
                 },
                 "a_not_analysed_property": {
                    "type": "string",
                    "index": "not_analyzed"
                 },
                 "a_date_property": {
                    "type": "date"
                 }
              }
           }
        }

        We cache the properties of each doc_type, if they are not available, we'll load them again from Elasticsearch
        """
        # Try loading the mapping from the cache.
        mapping = ElasticSearchEngine.get_mappings(self.index_name, doc_type)

        # Fall back to Elasticsearch
        if not mapping:
            mapping = self._es.indices.get_mapping(
                index=self.index_name,
                doc_type=doc_type,
            ).get(self.index_name, {}).get('mappings', {}).get(doc_type, {})

            # Cache the mapping, if one was retrieved
            if mapping:
                ElasticSearchEngine.set_mappings(
                    self.index_name,
                    doc_type,
                    mapping
                )

        return mapping
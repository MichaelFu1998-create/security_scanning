def index(self, doc_type, sources, **kwargs):
        """
        Implements call to add documents to the ES index
        Note the call to _check_mappings which will setup fields with the desired mappings
        """

        try:
            actions = []
            for source in sources:
                self._check_mappings(doc_type, source)
                id_ = source['id'] if 'id' in source else None
                log.debug("indexing %s object with id %s", doc_type, id_)
                action = {
                    "_index": self.index_name,
                    "_type": doc_type,
                    "_id": id_,
                    "_source": source
                }
                actions.append(action)
            # bulk() returns a tuple with summary information
            # number of successfully executed actions and number of errors if stats_only is set to True.
            _, indexing_errors = bulk(
                self._es,
                actions,
                **kwargs
            )
            if indexing_errors:
                ElasticSearchEngine.log_indexing_error(indexing_errors)
        # Broad exception handler to protect around bulk call
        except Exception as ex:
            # log information and re-raise
            log.exception("error while indexing - %s", str(ex))
            raise
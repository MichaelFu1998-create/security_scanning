def remove(self, doc_type, doc_ids, **kwargs):
        """ Implements call to remove the documents from the index """

        try:
            # ignore is flagged as an unexpected-keyword-arg; ES python client documents that it can be used
            # pylint: disable=unexpected-keyword-arg
            actions = []
            for doc_id in doc_ids:
                log.debug("Removing document of type %s and index %s", doc_type, doc_id)
                action = {
                    '_op_type': 'delete',
                    "_index": self.index_name,
                    "_type": doc_type,
                    "_id": doc_id
                }
                actions.append(action)
            bulk(self._es, actions, **kwargs)
        except BulkIndexError as ex:
            valid_errors = [error for error in ex.errors if error['delete']['status'] != 404]

            if valid_errors:
                log.exception("An error occurred while removing documents from the index.")
                raise
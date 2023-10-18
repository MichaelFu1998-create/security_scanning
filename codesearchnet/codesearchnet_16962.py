def set_bookmark(self):
        """Set bookmark for starting next aggregation."""
        def _success_date():
            bookmark = {
                'date': self.new_bookmark or datetime.datetime.utcnow().
                strftime(self.doc_id_suffix)
            }

            yield dict(_index=self.last_index_written,
                       _type=self.bookmark_doc_type,
                       _source=bookmark)
        if self.last_index_written:
            bulk(self.client,
                 _success_date(),
                 stats_only=True)
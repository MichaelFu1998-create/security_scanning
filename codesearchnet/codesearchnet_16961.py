def get_bookmark(self):
        """Get last aggregation date."""
        if not Index(self.aggregation_alias,
                     using=self.client).exists():
            if not Index(self.event_index,
                         using=self.client).exists():
                return datetime.date.today()
            return self._get_oldest_event_timestamp()

        # retrieve the oldest bookmark
        query_bookmark = Search(
            using=self.client,
            index=self.aggregation_alias,
            doc_type=self.bookmark_doc_type
        )[0:1].sort(
            {'date': {'order': 'desc'}}
        )
        bookmarks = query_bookmark.execute()
        # if no bookmark is found but the index exist, the bookmark was somehow
        # lost or never written, so restart from the beginning
        if len(bookmarks) == 0:
            return self._get_oldest_event_timestamp()

        # change it to doc_id_suffix
        bookmark = datetime.datetime.strptime(bookmarks[0].date,
                                              self.doc_id_suffix)
        return bookmark
def match(self, query=None, **kwargs):
        """Try to match the current record to the database."""
        from invenio.search_engine import perform_request_search
        if not query:
            # We use default setup
            recid = self.record["001"][0][3]
            return perform_request_search(p="035:%s" % (recid,),
                                          of="id")
        else:
            if "recid" not in kwargs:
                kwargs["recid"] = self.record["001"][0][3]
            return perform_request_search(p=query % kwargs,
                                          of="id")
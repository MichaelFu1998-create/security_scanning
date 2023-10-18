def key_info(self, **kwargs):
        """
        Retrieve info about the permissions associated with the
        key associated to the given Zotero instance
        """
        query_string = "/keys/{k}".format(k=self.api_key)
        return self._build_query(query_string)
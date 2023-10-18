def new_fulltext(self, version):
        """
        Retrieve list of full-text content items and versions which are newer
        than <version>
        """
        query_string = "/{t}/{u}/fulltext".format(
            t=self.library_type, u=self.library_id
        )
        headers = {"since": str(version)}
        headers.update(self.default_headers())
        req = requests.get(self.endpoint + query_string, headers=headers)
        try:
            req.raise_for_status()
        except requests.exceptions.HTTPError:
            error_handler(req)
        return req.json()
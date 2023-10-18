def set_fulltext(self, itemkey, payload):
        """"
        Set full-text data for an item
        <itemkey> should correspond to an existing attachment item.
        payload should be a dict containing three keys:
        'content': the full-text content and either
        For text documents, 'indexedChars' and 'totalChars' OR
        For PDFs, 'indexedPages' and 'totalPages'.

        """
        headers = self.default_headers()
        headers.update({"Content-Type": "application/json"})
        req = requests.put(
            url=self.endpoint
            + "/{t}/{u}/items/{k}/fulltext".format(
                t=self.library_type, u=self.library_id, k=itemkey
            ),
            headers=headers,
            data=json.dumps(payload),
        )
        try:
            req.raise_for_status()
        except requests.exceptions.HTTPError:
            error_handler(req)
        return True
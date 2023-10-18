def _merge_headers(self, call_specific_headers):
        """
        Merge headers from different sources together.  Headers passed to the
        post/get methods have highest priority, then headers associated with
        the connection object itself have next priority.

        :param call_specific_headers: A header dict from the get/post call, or
            None (the default for those methods).
        :return: A key-case-insensitive MutableMapping object which contains
            the merged headers.  (This doesn't actually return a dict.)
        """

        # A case-insensitive mapping is necessary here so that there is
        # predictable behavior.  If a plain dict were used, you'd get keys in
        # the merged dict which differ only in case.  The requests library
        # would merge them internally, and it would be unpredictable which key
        # is chosen for the final set of headers.  Another possible approach
        # would be to upper/lower-case everything, but this seemed easier.  On
        # the other hand, I don't know if CaseInsensitiveDict is public API...?

        # First establish defaults
        merged_headers = requests.structures.CaseInsensitiveDict({
            "User-Agent": self.user_agent
        })

        # Then overlay with specifics from post/get methods
        if call_specific_headers:
            merged_headers.update(call_specific_headers)

        # Special "User-Agent" header check, to ensure one is always sent.
        # The call-specific overlay could have null'd out that header.
        if not merged_headers.get("User-Agent"):
            merged_headers["User-Agent"] = self.user_agent

        return merged_headers
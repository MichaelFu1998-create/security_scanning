def search(self, terms):
        """ Search transcripts.

        Args:
            terms (str): Terms for search

        Returns:
            array. Messages
        """
        messages = self._connection.get("search/%s" % urllib.quote_plus(terms), key="messages")
        if messages:
            messages = [Message(self, message) for message in messages]
        return messages
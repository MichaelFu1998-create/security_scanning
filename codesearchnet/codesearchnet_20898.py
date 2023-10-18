def transcript(self, for_date=None):
        """ Recent messages.

        Kwargs:
            for_date (date): If specified, get the transcript for this specific date

        Returns:
            array. Messages
        """
        url = "room/%s/transcript" % self.id
        if for_date:
            url = "%s/%d/%d/%d" % (url, for_date.year, for_date.month, for_date.day)
        messages = self._connection.get(url, key="messages")
        if messages:
            messages = [Message(self._campfire, message) for message in messages]
        return messages
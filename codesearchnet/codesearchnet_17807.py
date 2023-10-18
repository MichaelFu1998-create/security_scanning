def url(self):
        """Returns the url of the poll. If the poll has not been submitted yet,
        an empty string is returned instead.
        """
        if self.id is None:
            return ''
        return '{}/{}'.format(strawpoll.API._BASE_URL, self.id)
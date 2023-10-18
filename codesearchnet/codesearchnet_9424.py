def get_source_by_nick(self, nick):
        """Returns the :class:`Source` of the given nick.

        :param str nick: nickname for which will be searched in the config
        """
        url = self.cfg.get("following", nick, fallback=None)
        return Source(nick, url) if url else None
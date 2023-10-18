def following(self):
        """A :class:`list` of all :class:`Source` objects."""
        following = []
        try:
            for (nick, url) in self.cfg.items("following"):
                source = Source(nick, url)
                following.append(source)
        except configparser.NoSectionError as e:
            logger.debug(e)

        return following
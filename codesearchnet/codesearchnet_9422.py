def options(self):
        """A :class:`dict` of all config options."""
        try:
            return dict(self.cfg.items("twtxt"))
        except configparser.NoSectionError as e:
            logger.debug(e)
            return {}
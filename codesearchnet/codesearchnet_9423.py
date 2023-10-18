def add_source(self, source):
        """Adds a new :class:`Source` to the config’s following section."""
        if not self.cfg.has_section("following"):
            self.cfg.add_section("following")

        self.cfg.set("following", source.nick, source.url)
        self.write_config()
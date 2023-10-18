def remove_source_by_nick(self, nick):
        """Removes a :class:`Source` form the config’s following section.

        :param str nick: nickname for which will be searched in the config
        """
        if not self.cfg.has_section("following"):
            return False

        ret_val = self.cfg.remove_option("following", nick)
        self.write_config()
        return ret_val
def colored_level_name(self, levelname):
        """
        Colors the logging level in the logging record
        """
        if self.colors_disabled:
            return self.plain_levelname_format.format(levelname)
        else:
            return self.colored_levelname_format.format(self.color_map[levelname], levelname)
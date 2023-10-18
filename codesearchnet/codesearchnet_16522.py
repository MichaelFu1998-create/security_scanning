def use_parser(self,parsername):
        """Set parsername as the current parser and apply it."""
        self.__parser = self.parsers[parsername]
        self.__parser()
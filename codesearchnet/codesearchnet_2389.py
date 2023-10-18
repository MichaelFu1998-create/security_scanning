def RemoveSearchProperties(self, **searchProperties) -> None:
        """
        searchProperties: dict, same as searchProperties in `Control.__init__`.
        """
        for key in searchProperties:
            del self.searchProperties[key]
            if key == 'RegexName':
                self.regexName = None
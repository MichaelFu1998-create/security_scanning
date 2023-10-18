def AddSearchProperties(self, **searchProperties) -> None:
        """
        Add search properties using `dict.update`.
        searchProperties: dict, same as searchProperties in `Control.__init__`.
        """
        self.searchProperties.update(searchProperties)
        if 'Depth' in searchProperties:
            self.searchDepth = searchProperties['Depth']
        if 'RegexName' in searchProperties:
            regName = searchProperties['RegexName']
            self.regexName = re.compile(regName) if regName else None
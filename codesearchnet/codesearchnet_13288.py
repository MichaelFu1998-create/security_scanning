def load_roster(self, source):
        """Load roster from an XML file.

        Can be used before the connection is started to load saved
        roster copy, for efficient retrieval of versioned roster.

        :Parameters:
            - `source`: file name or a file object
        :Types:
            - `source`: `str` or file-like object
        """
        try:
            tree = ElementTree.parse(source)
        except ElementTree.ParseError, err:
            raise ValueError("Invalid roster format: {0}".format(err))
        roster = Roster.from_xml(tree.getroot())
        for item in roster:
            item.verify_roster_result(True)
        self.roster = roster
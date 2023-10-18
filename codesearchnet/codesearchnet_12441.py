def add_intent(self, name, lines, reload_cache=False):
        """
        Creates a new intent, optionally checking the cache first

        Args:
            name (str): The associated name of the intent
            lines (list<str>): All the sentences that should activate the intent
            reload_cache: Whether to ignore cached intent if exists
        """
        self.intents.add(name, lines, reload_cache)
        self.padaos.add_intent(name, lines)
        self.must_train = True
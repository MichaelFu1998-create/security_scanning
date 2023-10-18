def load_intent(self, name, file_name, reload_cache=False):
        """
        Loads an intent, optionally checking the cache first

        Args:
            name (str): The associated name of the intent
            file_name (str): The location of the intent file
            reload_cache (bool): Whether to refresh all of cache
        """
        self.intents.load(name, file_name, reload_cache)
        with open(file_name) as f:
            self.padaos.add_intent(name, f.read().split('\n'))
        self.must_train = True
def remove_intent(self, name):
        """Unload an intent"""
        self.intents.remove(name)
        self.padaos.remove_intent(name)
        self.must_train = True
def discovery_view(self, message):
        """
        Use the new message to search for a registered view according
        to its pattern.
        """
        for handler in self.registered_handlers:
            if handler.check(message):
                return handler.view

        return None
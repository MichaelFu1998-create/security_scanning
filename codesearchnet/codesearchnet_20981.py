def wrap_handler(self, handler, context_switcher):
        """Enable/Disable handler."""
        context_switcher.add_context_in(lambda: LOGGER.addHandler(self.handler))
        context_switcher.add_context_out(lambda: LOGGER.removeHandler(self.handler))